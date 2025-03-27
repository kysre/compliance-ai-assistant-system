import json
import os
import time

from django.core.management.base import BaseCommand

from compliance.service import get_graph_rag_service
from utils.scraper import Scraper


class Command(BaseCommand):
    help = "Imports rules data from rules-data.json into the GraphRAG service"

    def add_arguments(self, parser):
        parser.add_argument(
            "--batch-size",
            type=int,
            default=100,
            help="Number of rules to process in each batch",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Maximum number of rules to process (default: process all)",
        )

    def handle(self, *args, **options):
        batch_size = options["batch_size"]
        limit = options["limit"]
        self.stdout.write(
            self.style.SUCCESS(f"Starting import with batch size: {batch_size}")
        )
        if limit:
            self.stdout.write(self.style.SUCCESS(f"Limiting import to {limit} rules"))

        data_file_path = Scraper.get_all_rules_data_path()
        if not os.path.exists(data_file_path):
            self.stdout.write(
                self.style.ERROR(f"Rules data file not found at: {data_file_path}")
            )
            return

        try:
            rag_service = get_graph_rag_service()
            self.stdout.write(
                self.style.SUCCESS("Successfully initialized GraphRAG service")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to initialize GraphRAG service: {str(e)}")
            )
            return

        try:
            with open(data_file_path, "r", encoding="utf-8") as f:
                rules_data = json.load(f)
                total_rules = len(rules_data)
                if limit and limit < total_rules:
                    rules_data = rules_data[:limit]
                    total_rules = limit
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully loaded {total_rules} rules from file"
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to load rules data: {str(e)}"))
            return

        start_time = time.time()
        processed_count = 0
        error_count = 0
        for i, rule in enumerate(rules_data):
            try:
                document = {
                    "id": rule.get("id", ""),
                    "title": rule.get("title", ""),
                    "content": rule.get("text", ""),
                    "date": rule.get("date", ""),
                    "authority": rule.get("authority", ""),
                    "link": rule.get("link", ""),
                }

                if not document["content"].strip():
                    self.stdout.write(
                        self.style.WARNING(f'Skipping empty rule: {document["title"]}')
                    )
                    continue

                rag_service.insert(str(document))
                processed_count += 1

                if (i + 1) % batch_size == 0 or (i + 1) == total_rules:
                    elapsed_time = time.time() - start_time
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Processed {i + 1}/{total_rules} rules "
                            f"({(i + 1) / total_rules * 100:.1f}%) "
                            f"in {elapsed_time:.2f} seconds"
                        )
                    )
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f"Error processing rule {i+1}: {str(e)}")
                )
                continue

        total_time = time.time() - start_time
        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed in {total_time:.2f} seconds. "
                f"Successfully processed {processed_count} rules with {error_count} errors."
            )
        )
