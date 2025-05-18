import time

from lightrag import QueryParam
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .service import GRAPH_RAG_MODES, get_graph_rag_service
from .models import Regulation
from .serializers import RegulationSerializer


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
        rag_service = get_graph_rag_service()
        rag_service.insert(
            documents=[
                str(
                    {
                        "title": validated_data["title"],
                        "text": validated_data["text"],
                        "authority": validated_data["authority"],
                        "date": validated_data["date"],
                    }
                )
            ],
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

    results = {"successful": [], "failed": []}

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

        for serializer in valid_regulations:
            validated_data = serializer.validated_data
            documents.append(
                str(
                    {
                        "title": validated_data["title"],
                        "text": validated_data["text"],
                        "authority": validated_data["authority"],
                        "date": validated_data["date"],
                    }
                )
            )
            ids.append(validated_data["identifier"])
            file_paths.append(validated_data.get("link", ""))

        # Insert all documents into RAG service
        rag_service.insert(
            documents=documents,
            ids=ids,
            file_paths=file_paths,
        )

        # Save all valid regulations to database
        for serializer in valid_regulations:
            serializer.save()
            results["successful"].append(serializer.validated_data["identifier"])

        return Response(
            {
                "message": f"Successfully inserted {len(valid_regulations)} of {len(regulations_data)} documents",
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


@api_view(["GET"])
def query(request):
    """
    API endpoint to query the GraphRAG service.

    Expects a JSON payload with:
    {
        "query": "The query to ask the GraphRAG service"
    }

    Returns a JSON response with:
    {
        "results": [
            {
                "mode": "The mode of the query",
                "result": "The result of the query",
                "time": "The time it took to run the query"
            },
            ...
        ]
    }
    """
    query = request.data.get("query", None)
    if not query:
        return Response(
            {"error": "query is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        # Get the RAG service
        rag_service = get_graph_rag_service()
        # Query the rag service with all modes
        results = []
        for mode in GRAPH_RAG_MODES:
            start_time = time.time()
            result = rag_service.query(query, param=QueryParam(mode=mode))
            exec_time = time.time() - start_time
            results.append(
                {
                    "mode": mode,
                    "result": result,
                    "time": f"{exec_time:.4f}",
                }
            )
        return Response(
            {
                "results": results,
            }
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
