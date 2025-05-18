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
            str(
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
