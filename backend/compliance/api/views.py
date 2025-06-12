import json
import time

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from compliance.api.serializers import RegulationSerializer
from compliance.models import Regulation
from compliance.service import LightRagClient, LightRagMode


class RegulationPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class RegulationListView(APIView):
    """
    API endpoint for managing regulations collection.

    GET Request:
        Returns a paginated list of regulations without their full text content.

        Request Sample:
            GET /api/compliance/regulations/?page=1&page_size=20

        Response (200 OK):
            {
                "count": <total_count>,
                "next": "<next_page_url>",
                "previous": "<previous_page_url>",
                "results": [
                    {
                        "identifier": "REG-001",
                        "title": "Sample Regulation",
                        "date": "2024-01-01",
                        "authority": "Sample Authority",
                        "link": "https://example.com/regulation"
                        // Note: text field is excluded for performance
                    },
                    ...
                ]
            }

    POST Request:
        Creates a new regulation in the system.

        Request Body:
            {
                "identifier": "Unique regulation identifier (required)",
                "title": "Regulation title (required)",
                "text": "Full regulation text (required)",
                "date": "Regulation date (required)",
                "authority": "Issuing authority (required)",
                "link": "URL to regulation source (optional)"
            }
    """

    def get(self, request):
        regulations = Regulation.objects.all()
        paginator = RegulationPagination()
        paginated_regulations = paginator.paginate_queryset(regulations, request)
        serializer = RegulationSerializer(
            paginated_regulations, many=True, context={"include_text": False}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = RegulationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            validated_data = serializer.validated_data
            if Regulation.objects.filter(
                identifier=validated_data["identifier"]
            ).exists():
                return Response(
                    {"message": "Regulation with this identifier already exists"},
                    status=status.HTTP_200_OK,
                )
            # TODO: insert into different rags
            serializer.save()
            return Response(
                {"message": "Regulation inserted successfully"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegulationView(APIView):
    """
    API endpoint for managing individual regulations.

    GET Request:
        Retrieves a single regulation by its unique identifier, including full text content.

        Request Sample:
            GET /api/compliance/regulations/REGULATION-ID/

        Response (200 OK):
            {
                "regulation": {
                    "identifier": "REGULATION-ID",
                    "title": "Sample Regulation",
                    "text": "Full regulation text content...",
                    "date": "2024-01-01",
                    "authority": "Sample Authority",
                    "link": "https://example.com/regulation"
                }
            }

    DELETE Request:
        Removes a regulation from the system and RAG service.

        Request Sample:
            DELETE /api/compliance/regulations/REGULATION-ID/
    """

    def get(self, request, identifier):
        try:
            regulation = Regulation.objects.get(identifier=identifier)
        except Regulation.DoesNotExist:
            return Response(
                {"error": "Regulation not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = RegulationSerializer(regulation, context={"include_text": True})
        return Response({"regulation": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, identifier):
        try:
            regulation = Regulation.objects.get(identifier=identifier)
        except Regulation.DoesNotExist:
            return Response(
                {"error": "Regulation not found"}, status=status.HTTP_404_NOT_FOUND
            )
        # TODO: Implement delete api and remove regulation from rags
        # regulation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def insert(request):
    """
    API endpoint to insert a document into the GraphRAG service and database.

    Expects a JSON payload with regulation data including:
    {
        "identifier": "Unique identifier",
        "title": "Regulation title",
        "text": "Full regulation text",
        "date": "Regulation date",
        "authority": "Approving authority",
        "link": "URL to regulation"
    }
    """
    serializer = RegulationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    try:
        validated_data = serializer.validated_data
        if Regulation.objects.filter(identifier=validated_data["identifier"]).exists():
            return Response(
                {"message": "Regulation with this identifier already exists"},
                status=status.HTTP_200_OK,
            )
        lightrag_client = LightRagClient()
        lightrag_client.insert_texts(
            texts=[
                json.dumps(
                    {
                        "title": validated_data["title"],
                        "text": validated_data["text"],
                        "authority": validated_data["authority"],
                        "date": validated_data["date"],
                    }
                )
            ],
            ids=[validated_data["identifier"]],
            sources=[validated_data.get("link", "")],
        )
        serializer.save()
        return Response(
            {"message": "Document inserted successfully"}, status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def batch_insert(request):
    """
    API endpoint to insert multiple documents into the GraphRAG service and database.

    Expects a JSON payload with an array of regulation data:
    {
        "regulations": [
            {
                "identifier": "Unique identifier 1",
                "title": "Regulation title 1",
                "text": "Full regulation text 1",
                "date": "Regulation date 1",
                "authority": "Approving authority 1",
                "link": "URL to regulation 1"
            },
            {
                "identifier": "Unique identifier 2",
                "title": "Regulation title 2",
                "text": "Full regulation text 2",
                "date": "Regulation date 2",
                "authority": "Approving authority 2",
                "link": "URL to regulation 2"
            },
            ...
        ]
    }
    """
    regulations_data = request.data.get("regulations", [])
    if not regulations_data or not isinstance(regulations_data, list):
        return Response(
            {"error": "regulations array is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    results = {"successful": [], "failed": [], "skipped": []}

    # Validate all regulations first
    valid_regulations = []
    for i, reg_data in enumerate(regulations_data):
        serializer = RegulationSerializer(data=reg_data)
        if serializer.is_valid():
            valid_regulations.append(serializer)
        else:
            results["failed"].append(
                {"index": i, "data": reg_data, "errors": serializer.errors}
            )

    # If no valid regulations, return early
    if not valid_regulations:
        return Response(
            {"message": "No valid regulations found", "results": results},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        # Prepare data for bulk insert to RAG service
        documents = []
        ids = []
        file_paths = []
        regulation_instances = []

        # Check for existing regulations and filter them out
        for serializer in valid_regulations:
            validated_data = serializer.validated_data
            identifier = validated_data["identifier"]

            # Skip if regulation with this identifier already exists
            if Regulation.objects.filter(identifier=identifier).exists():
                results["skipped"].append(
                    {"identifier": identifier, "reason": "Already exists"}
                )
                continue

            documents.append(
                json.dumps(
                    {
                        "title": validated_data["title"],
                        "text": validated_data["text"],
                        "authority": validated_data["authority"],
                        "date": validated_data["date"],
                    }
                )
            )
            ids.append(identifier)
            file_paths.append(validated_data.get("link", ""))

            instance = Regulation(
                identifier=identifier,
                title=validated_data["title"],
                text=validated_data["text"],
                date=validated_data["date"],
                authority=validated_data["authority"],
                link=validated_data.get("link", ""),
            )
            regulation_instances.append(instance)
            results["successful"].append(identifier)

        # If no new regulations to insert, return early
        if not documents:
            return Response(
                {
                    "message": "No new regulations to insert, all already exist",
                    "results": results,
                },
                status=status.HTTP_200_OK,
            )

        with transaction.atomic():
            lightrag = LightRagClient()
            lightrag.insert(
                documents,
                ids=ids,
                file_paths=file_paths,
            )
            Regulation.objects.bulk_create(regulation_instances)

        return Response(
            {
                "message": f"Successfully inserted {len(regulation_instances)} of {len(regulations_data)} documents, {len(results['skipped'])} documents skipped",
                "results": results,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        # Add any successful inserts to failed list since we had an exception
        for serializer in valid_regulations:
            if serializer.validated_data["identifier"] not in results["successful"]:
                results["failed"].append(
                    {
                        "identifier": serializer.validated_data["identifier"],
                        "error": "Failed during insertion",
                    }
                )

        return Response(
            {"error": str(e), "results": results},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
def query(request):
    """
    API endpoint to query the GraphRAG service.

    Expects a JSON payload with:
    {
        "mode": "The mode of the query",
        "query": "The query to ask the GraphRAG service"
    }

    Returns a JSON response with:
    {
        "text": "The result of the query",
        "time": "The time it took to run the query"
    }
    """
    query = request.data.get("query", None)
    if not query:
        return Response(
            {"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    mode = request.data.get("mode", None)
    if not mode:
        mode = "naive"
    mode = LightRagMode(mode)
    try:
        lightrag = LightRagClient()
        start_time = time.time()
        result = lightrag.query(query, mode=mode)
        exec_time = time.time() - start_time
        return Response(
            {
                "text": result,
                "time": f"{exec_time:.4f}",
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
