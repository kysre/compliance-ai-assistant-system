import asyncio
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from django.core.management.base import BaseCommand
from django.db import transaction

from compliance.api.serializers import RegulationSerializer
from compliance.models import Regulation
from utils.scraper import Scraper

# Constants
DEFAULT_BATCH_SIZE = 5
DEFAULT_WORKERS = 1
DEFAULT_START_INDEX = 0

ALLOWED_AUTHORITIES = [
    "شوراي اقتصاد",
    "سازمان امور مالياتي",
    "وزارت امور اقتصادي و دارايي",
    "وزير امور اقتصادي و دارايي",
]

PROGRESS_UPDATE_FIELDS = ["successful", "failed", "skipped"]


@dataclass
class ImportConfig:
    """Configuration for the import process."""

    batch_size: int
    start_index: int
    limit: Optional[int]
    max_workers: int


@dataclass
class ImportResults:
    """Results of the import process."""

    successful: List[Any]
    failed: List[Any]
    skipped: List[Any]

    def __init__(self):
        self.successful = []
        self.failed = []
        self.skipped = []

    def add_successful(self, items: List[Any]) -> None:
        self.successful.extend(items)

    def add_failed(self, items: List[Any]) -> None:
        self.failed.extend(items)

    def add_skipped(self, items: List[Any]) -> None:
        self.skipped.extend(items)

    def get_total_processed(self) -> int:
        return len(self.successful) + len(self.failed) + len(self.skipped)


class RulesDataLoader:
    """Handles loading and filtering of rules data."""

    @staticmethod
    def load_rules_from_file() -> List[Dict[str, Any]]:
        """Load rules data from the JSON file."""
        data_file_path = Scraper.get_all_rules_data_path()

        try:
            with open(data_file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Rules data file not found at: {data_file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON from {data_file_path}: {str(e)}")

    @staticmethod
    def filter_rules_by_authority(rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter rules by allowed authorities."""
        filtered_rules = []
        for rule in rules:
            authority = rule.get("authority", "").strip()
            if authority in ALLOWED_AUTHORITIES:
                filtered_rules.append(rule)
        return filtered_rules

    @staticmethod
    def slice_rules_data(
        rules: List[Dict[str, Any]], config: ImportConfig
    ) -> List[Dict[str, Any]]:
        """Apply start index and limit to rules data."""
        if config.start_index >= len(rules):
            return []

        rules_after_start = rules[config.start_index :]

        if config.limit is not None:
            return rules_after_start[: config.limit]

        return rules_after_start


class RegulationValidator:
    """Handles validation of regulation data."""

    @staticmethod
    def create_regulation_data(rule: Dict[str, Any]) -> Dict[str, Any]:
        """Create regulation data from rule."""
        return {
            "identifier": rule.get("id", ""),
            "title": rule.get("title", ""),
            "text": rule.get("text", ""),
            "date": rule.get("date", ""),
            "authority": rule.get("authority", ""),
            "link": rule.get("link", ""),
        }

    @staticmethod
    def validate_regulations(
        regulations_data: List[Dict[str, Any]]
    ) -> tuple[List[RegulationSerializer], List[Dict[str, Any]]]:
        """Validate regulations data and return valid serializers and failed items."""
        valid_serializers = []
        failed_items = []

        for reg_data in regulations_data:
            serializer = RegulationSerializer(data=reg_data)
            if serializer.is_valid():
                valid_serializers.append(serializer)
            else:
                failed_items.append(
                    {
                        "identifier": reg_data.get("identifier", "UNKNOWN_ID"),
                        "input_data": reg_data,
                        "reason": "Validation Error",
                        "errors": serializer.errors,
                    }
                )

        return valid_serializers, failed_items


class RegulationProcessor:
    """Processes regulations for database and RAG insertion."""

    def __init__(self):
        self.results_lock = threading.Lock()
        self.results = ImportResults()

    def process_batch(self, batch: List[Dict[str, Any]]) -> None:
        """Process a batch of rules."""
        thread_local_results = ImportResults()

        # Create regulation data
        regulations_data = [
            RegulationValidator.create_regulation_data(rule) for rule in batch
        ]

        # Validate regulations
        valid_serializers, failed_items = RegulationValidator.validate_regulations(
            regulations_data
        )
        thread_local_results.add_failed(failed_items)

        if not valid_serializers:
            self._update_results(thread_local_results)
            return

        # Process valid regulations
        self._process_valid_regulations(valid_serializers, thread_local_results)
        self._update_results(thread_local_results)

    def _process_valid_regulations(
        self,
        valid_serializers: List[RegulationSerializer],
        thread_local_results: ImportResults,
    ) -> None:
        """Process valid regulations for insertion."""
        regulation_instances = []
        rag_documents = []
        rag_ids = []
        rag_file_paths = []
        identifiers_for_insertion = []

        for serializer in valid_serializers:
            validated_data = serializer.validated_data
            identifier = validated_data["identifier"]

            if self._should_skip_regulation(
                validated_data, identifier, thread_local_results
            ):
                continue

            self._prepare_regulation_for_insertion(
                validated_data,
                identifier,
                regulation_instances,
                rag_documents,
                rag_ids,
                rag_file_paths,
                identifiers_for_insertion,
            )

        if regulation_instances:
            self._insert_regulations(
                regulation_instances,
                rag_documents,
                rag_ids,
                rag_file_paths,
                identifiers_for_insertion,
                thread_local_results,
            )

    def _should_skip_regulation(
        self,
        validated_data: Dict[str, Any],
        identifier: str,
        thread_local_results: ImportResults,
    ) -> bool:
        """Check if regulation should be skipped."""
        if Regulation.objects.filter(identifier=identifier).exists():
            thread_local_results.add_skipped(
                [{"identifier": identifier, "reason": "Already exists in DB"}]
            )
            return True

        if not validated_data.get("text", "").strip():
            thread_local_results.add_skipped(
                [{"identifier": identifier, "reason": "Empty content"}]
            )
            return True

        return False

    def _prepare_regulation_for_insertion(
        self,
        validated_data: Dict[str, Any],
        identifier: str,
        regulation_instances: List[Regulation],
        rag_documents: List[str],
        rag_ids: List[str],
        rag_file_paths: List[str],
        identifiers_for_insertion: List[str],
    ) -> None:
        """Prepare regulation data for insertion."""
        identifiers_for_insertion.append(identifier)

        rag_documents.append(
            json.dumps(
                {
                    "title": validated_data.get("title", ""),
                    "text": validated_data.get("text", ""),
                    "authority": validated_data.get("authority", ""),
                    "date": validated_data.get("date", ""),
                }
            )
        )

        rag_ids.append(identifier)
        rag_file_paths.append(validated_data.get("link", ""))
        regulation_instances.append(Regulation(**validated_data))

    def _insert_regulations(
        self,
        regulation_instances: List[Regulation],
        rag_documents: List[str],
        rag_ids: List[str],
        rag_file_paths: List[str],
        identifiers_for_insertion: List[str],
        thread_local_results: ImportResults,
    ) -> None:
        """Insert regulations into database and RAG service."""
        try:
            from compliance.service import GraphRagService

            rag_service = GraphRagService()
            rag_service = asyncio.run(rag_service.initialize_rag())

            with transaction.atomic():
                rag_service.insert(
                    rag_documents, ids=rag_ids, file_paths=rag_file_paths
                )
                Regulation.objects.bulk_create(regulation_instances)

            thread_local_results.add_successful(identifiers_for_insertion)

        except Exception as e:
            failed_items = [
                {
                    "identifier": identifier,
                    "reason": "Insertion Error",
                    "details": str(e),
                }
                for identifier in identifiers_for_insertion
            ]
            thread_local_results.add_failed(failed_items)

    def _update_results(self, thread_local_results: ImportResults) -> None:
        """Thread-safe update of global results."""
        with self.results_lock:
            self.results.add_successful(thread_local_results.successful)
            self.results.add_failed(thread_local_results.failed)
            self.results.add_skipped(thread_local_results.skipped)


class ImportProgressTracker:
    """Tracks and reports import progress."""

    def __init__(self, total_rules: int, start_time: float):
        self.total_rules = total_rules
        self.start_time = start_time

    def report_batch_completion(
        self, completed_batches: int, total_batches: int, results: ImportResults, stdout
    ) -> None:
        """Report batch completion progress."""
        total_processed = results.get_total_processed()
        elapsed_time = time.time() - self.start_time
        progress_percentage = (
            (total_processed / self.total_rules * 100) if self.total_rules > 0 else 0
        )

        stdout.write(
            f"Completed {completed_batches}/{total_batches} batches. "
            f"Rules processed: {total_processed}/{self.total_rules} ({progress_percentage:.1f}%). "
            f"Elapsed: {elapsed_time:.2f}s. "
            f"(Success: {len(results.successful)}, Failed: {len(results.failed)}, Skipped: {len(results.skipped)})"
        )

    def report_final_results(self, results: ImportResults, stdout) -> None:
        """Report final import results."""
        total_time = time.time() - self.start_time
        stdout.write(
            f"Import completed in {total_time:.2f} seconds. "
            f"Successfully processed: {len(results.successful)}, "
            f"Skipped: {len(results.skipped)}, "
            f"Failed: {len(results.failed)}."
        )


class Command(BaseCommand):
    help = (
        "Imports rules data from rules-data.json into the database and GraphRAG service"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=DEFAULT_BATCH_SIZE,
            help="Number of rules to process in each batch",
        )
        parser.add_argument(
            "--start",
            type=int,
            default=DEFAULT_START_INDEX,
            help="Start index for processing rules",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of rules to process (default: process all)",
        )
        parser.add_argument(
            "--workers",
            type=int,
            default=DEFAULT_WORKERS,
            help="Number of worker threads to use for parallel processing",
        )

    def handle(self, *args, **options):
        config = self._create_config(options)

        if not self._validate_config(config):
            return

        try:
            rules_data = self._load_and_prepare_data(config)
        except (FileNotFoundError, ValueError) as e:
            self.stdout.write(self.style.ERROR(str(e)))
            return

        if not rules_data:
            self.stdout.write(self.style.SUCCESS("No rules to process."))
            return

        self._execute_import(rules_data, config)

    def _create_config(self, options: Dict[str, Any]) -> ImportConfig:
        """Create import configuration from command options."""
        return ImportConfig(
            batch_size=options["batch_size"],
            start_index=options["start"],
            limit=options["limit"],
            max_workers=options["workers"],
        )

    def _validate_config(self, config: ImportConfig) -> bool:
        """Validate import configuration."""
        if config.start_index < 0:
            self.stdout.write(self.style.ERROR("Start index cannot be negative."))
            return False

        if config.limit is not None and config.limit <= 0:
            self.stdout.write(
                self.style.ERROR("Limit must be a positive integer if provided.")
            )
            return False

        return True

    def _load_and_prepare_data(self, config: ImportConfig) -> List[Dict[str, Any]]:
        """Load and prepare rules data for processing."""
        # Load rules from file
        all_rules = RulesDataLoader.load_rules_from_file()

        # Filter by authority
        filtered_rules = RulesDataLoader.filter_rules_by_authority(all_rules)

        # Check start index bounds
        if config.start_index >= len(filtered_rules):
            self.stdout.write(
                self.style.WARNING(
                    f"Start index {config.start_index} is out of bounds for "
                    f"{len(filtered_rules)} filtered rules."
                )
            )
            return []

        # Apply start and limit
        return RulesDataLoader.slice_rules_data(filtered_rules, config)

    def _execute_import(
        self, rules_data: List[Dict[str, Any]], config: ImportConfig
    ) -> None:
        """Execute the import process."""
        total_rules = len(rules_data)
        self.stdout.write(
            self.style.SUCCESS(
                f"Processing {total_rules} rules (batch size: {config.batch_size}, "
                f"workers: {config.max_workers})"
            )
        )

        start_time = time.time()
        processor = RegulationProcessor()
        progress_tracker = ImportProgressTracker(total_rules, start_time)

        batches = self._create_batches(rules_data, config.batch_size)
        self._process_batches_in_parallel(
            batches, config.max_workers, processor, progress_tracker
        )

        progress_tracker.report_final_results(processor.results, self.style.SUCCESS)

    def _create_batches(
        self, rules_data: List[Dict[str, Any]], batch_size: int
    ) -> List[List[Dict[str, Any]]]:
        """Create batches from rules data."""
        return [
            rules_data[i : i + batch_size]
            for i in range(0, len(rules_data), batch_size)
        ]

    def _process_batches_in_parallel(
        self,
        batches: List[List[Dict[str, Any]]],
        max_workers: int,
        processor: RegulationProcessor,
        progress_tracker: ImportProgressTracker,
    ) -> None:
        """Process batches in parallel using thread pool."""
        actual_workers = min(max_workers, len(batches)) if batches else 1

        with ThreadPoolExecutor(max_workers=actual_workers) as executor:
            futures = [
                executor.submit(processor.process_batch, batch) for batch in batches
            ]

            completed_batches = 0
            total_batches = len(futures)

            for future in as_completed(futures):
                try:
                    future.result()
                    completed_batches += 1

                    with processor.results_lock:
                        progress_tracker.report_batch_completion(
                            completed_batches,
                            total_batches,
                            processor.results,
                            self.style.SUCCESS,
                        )

                except Exception as exc:
                    completed_batches += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f"Batch failed: {str(exc)}. Progress: {completed_batches}/{total_batches}"
                        )
                    )
