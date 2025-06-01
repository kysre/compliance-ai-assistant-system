import uuid

from django.contrib.auth import get_user_model
from django.db import models


class MessageRole(models.TextChoices):
    USER = "user", "User"
    ASSISTANT = "assistant", "Assistant"


class ChatUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Chat User"
        verbose_name_plural = "Chat Users"

    def __str__(self):
        return self.user.username


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_user = models.ForeignKey(
        ChatUser, on_delete=models.CASCADE, related_name="threads"
    )
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["chat_user", "-updated_at"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.chat_user.user.username}"

    @property
    def message_count(self):
        """Return the number of messages in this thread."""
        return self.messages.count()

    @property
    def latest_message(self):
        """Return the most recent message in this thread."""
        return self.messages.order_by("-created_at").first()


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(
        max_length=10,
        choices=MessageRole.choices,
        default=MessageRole.USER,
    )
    system_prompt = models.TextField(blank=True, default="")
    content = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["thread", "created_at"]),
            models.Index(fields=["role", "created_at"]),
        ]

    def __str__(self):
        content_preview = (
            self.content[:50] + "..." if len(self.content) > 50 else self.content
        )
        return f"{self.get_role_display()}: {content_preview}"
