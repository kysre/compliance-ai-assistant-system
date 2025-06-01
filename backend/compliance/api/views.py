import json
import time

from django.db import transaction
from lightrag import QueryParam
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from compliance.api.serializers import RegulationSerializer
from compliance.models import Regulation
from compliance.service import get_graph_rag_service


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
        rag_service = get_graph_rag_service()
        rag_service.insert(
            json.dumps(
                {
                    "title": validated_data["title"],
                    "text": validated_data["text"],
                    "authority": validated_data["authority"],
                    "date": validated_data["date"],
                }
            ),
            ids=[validated_data["identifier"]],
            file_paths=[validated_data.get("link", "")],
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
        rag_service = get_graph_rag_service()

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
            rag_service.insert(
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
    try:
        # Get the RAG service
        rag_service = get_graph_rag_service()
        # Query the rag service with all modes
        results = []
        start_time = time.time()
        result = rag_service.query(query, param=QueryParam(mode=mode))
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
