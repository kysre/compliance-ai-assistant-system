import time

from lightrag import QueryParam
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .service import GRAPH_RAG_MODES, get_graph_rag_service


@api_view(["POST"])
def insert(request):
    """
    API endpoint to insert a document into the GraphRAG service.

    Expects a JSON payload with:
    {
        "document": "The document to insert into the GraphRAG service"
    }
    """
    document = request.data.get("document", None)
    if not document:
        return Response(
            {"error": "document is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        # Get the RAG service
        rag_service = get_graph_rag_service()
        # Insert the document into the GraphRAG service
        rag_service.insert(document)
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
