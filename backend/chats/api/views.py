from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from chats.api.serializers import ThreadSerializer, UserSerializer, MessageSerializer
from chats.models import ChatUser, Thread, Message


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
        return Response({"token": token.key}, status=status.HTTP_200_OK)
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_messages(request, thread_id):
    thread = Thread.objects.get(id=thread_id)
    messages = Message.objects.filter(thread=thread).order_by("created_at").all()
    serializer = MessageSerializer(messages, many=True)
    return Response({"messages": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_message(request):
    pass
