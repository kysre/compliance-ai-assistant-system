from django.contrib.auth import get_user_model
from rest_framework import serializers

from chats.models import ChatUser, Message, Thread


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = get_user_model().objects.create(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class ChatUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = ChatUser
        fields = ("username", "email")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "role", "content", "created_at")


class ThreadSerializer(serializers.ModelSerializer):
    lastMessage = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source="created_at")

    class Meta:
        model = Thread
        fields = ("id", "title", "lastMessage", "createdAt")

    def get_lastMessage(self, obj):
        latest_message = obj.latest_message
        if latest_message:
            return MessageSerializer(latest_message).data
        return None
