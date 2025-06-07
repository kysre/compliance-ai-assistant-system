import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class MessageRole(models.TextChoices):
    USER = "user", _("User")
    ASSISTANT = "assistant", _("Assistant")


class ChatUser(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, verbose_name=_("User")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Chat User")
        verbose_name_plural = _("Chat Users")

    def __str__(self):
        return self.user.username


class Thread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_user = models.ForeignKey(
        ChatUser,
        on_delete=models.CASCADE,
        related_name="threads",
        verbose_name=_("Chat User"),
    )
    title = models.CharField(
        max_length=255, default=_("New Chat"), verbose_name=_("Title")
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Thread")
        verbose_name_plural = _("Threads")
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
        Thread,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("Thread"),
    )
    role = models.CharField(
        max_length=10,
        choices=MessageRole.choices,
        default=MessageRole.USER,
        verbose_name=_("Role"),
    )
    system_prompt = models.TextField(
        blank=True, default="", verbose_name=_("System Prompt")
    )
    content = models.TextField(blank=True, default="", verbose_name=_("Content"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
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
