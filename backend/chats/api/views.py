import time

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from chats.api.serializers import MessageSerializer, ThreadSerializer, UserSerializer
from chats.models import ChatUser, Message, MessageRole, Thread
from compliance.service import LightRagClient, LightRagMode


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    user_serializer = UserSerializer(data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        ChatUser.objects.create(user=user)
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user": {
                    "email": user.email,
                    "username": user.username,
                    "firstname": user.first_name,
                    "lastname": user.last_name,
                },
            },
            status=status.HTTP_200_OK,
        )
    return Response(
        {"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


class ThreadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        chat_user = ChatUser.objects.get(user=request.user)
        threads = (
            Thread.objects.filter(chat_user=chat_user).order_by("-updated_at").all()
        )
        serializer = ThreadSerializer(threads, many=True)
        return Response({"threads": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        chat_user = ChatUser.objects.get(user=request.user)
        empty_thread = (
            Thread.objects.filter(chat_user=chat_user)
            .filter(messages__isnull=True)
            .order_by("-updated_at")
            .first()
        )
        if empty_thread:
            thread = empty_thread
        else:
            thread = Thread.objects.create(chat_user=chat_user)
        serializer = ThreadSerializer(thread)
        return Response({"thread": serializer.data}, status=status.HTTP_201_CREATED)


class MessageView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, thread_id):
        thread = Thread.objects.get(id=thread_id)
        messages = Message.objects.filter(thread=thread).order_by("created_at").all()
        serializer = MessageSerializer(messages, many=True)
        return Response({"messages": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, thread_id):
        """
        API endpoint to send a message to the GraphRAG service.

        Expects a JSON payload with:
        {
            "type": "Type of rag service to use",
            "mode": "The mode of the query",
            "message": "The message to send to the rag service"
        }

        Returns a JSON response with:
        {
            "text": "The result of the query",
        }
        """
        message = request.data.get("message", None)
        if not message:
            return Response(
                {"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        thread = Thread.objects.get(id=thread_id)
        if not thread:
            return Response(
                {"error": "thread not found"}, status=status.HTTP_404_NOT_FOUND
            )
        rag_type = request.data.get("type", None)
        if not rag_type:
            rag_type = "lightrag"
        rag_mode = request.data.get("mode", None)
        if not rag_mode:
            rag_mode = "naive"
        try:
            start_time = time.time()
            if rag_type == "lightrag":
                lightrag = LightRagClient()
                mode = LightRagMode(rag_mode)
                result = lightrag.query(message, mode)
            exec_time = time.time() - start_time
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        Message.objects.create(
            thread=thread,
            content=message,
            role=MessageRole.USER,
        )
        Message.objects.create(
            thread=thread,
            content=result,
            role=MessageRole.ASSISTANT,
        )
        # TODO: make this prometheus metric
        print(f"exec_time: {exec_time:.4f}")
        return Response(
            {
                "text": result,
            },
            status=status.HTTP_200_OK,
        )
