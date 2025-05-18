import time

from lightrag import QueryParam
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .service import GRAPH_RAG_MODES, get_graph_rag_service
from .models import Regulation


@api_view(["POST"])
def insert(request):
    """
    API endpoint to insert a document into the GraphRAG service.

    Expects a JSON payload with:
    {
        "document": "The document to insert into the GraphRAG service"
    }
    """
    identifier = request.data.get("id")
    if not identifier:
        return Response(
            {"error": "IDS is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    text = request.data.get("text")
    if not text:
        return Response(
            {"error": "text is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    title = request.data.get("title")
    if not title:
        return Response(
            {"error": "title is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    date = request.data.get("date", "")
    date = date.replace("/", "-")
    if not date:
        return Response(
            {"error": "date is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    authority = request.data.get("authority", "")
    link = request.data.get("link", "")
    try:
        # Get the RAG service
        rag_service = get_graph_rag_service()
        # Insert the document into the GraphRAG service
        rag_service.insert(
            str(
                {
                    "title": title,
                    "text": text,
                    "authority": authority,
                    "date": date,
                }
            ),
            ids=[identifier],
            file_paths=[link],
        )
        Regulation.objects.create(
            identifier=identifier,
            title=title,
            date=date,
            authority=authority,
            link=link,
            text=text,
        )
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
