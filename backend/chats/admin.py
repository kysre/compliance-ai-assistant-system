from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ChatUser, Message, Thread


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "user_email",
        "user_first_name",
        "user_last_name",
        "created_at",
        "updated_at",
    )
    list_filter = ("user__is_active", "user__date_joined", "created_at", "updated_at")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = ("user", "created_at", "updated_at")

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = _("Email")

    def user_first_name(self, obj):
        return obj.user.first_name

    user_first_name.short_description = _("First Name")

    def user_last_name(self, obj):
        return obj.user.last_name

    user_last_name.short_description = _("Last Name")


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "chat_user",
        "message_count",
        "latest_message_preview",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at", "chat_user")
    search_fields = ("title", "chat_user__user__username", "chat_user__user__email")
    readonly_fields = (
        "id",
        "message_count",
        "latest_message",
        "created_at",
        "updated_at",
    )
    ordering = ("-updated_at",)

    def latest_message_preview(self, obj):
        latest = obj.latest_message
        if latest:
            content_preview = (
                latest.content[:50] + "..."
                if len(latest.content) > 50
                else latest.content
            )
            return f"{latest.get_role_display()}: {content_preview}"
        return _("No messages")

    latest_message_preview.short_description = _("Latest Message")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "thread",
        "role",
        "content_preview",
        "created_at",
        "updated_at",
    )
    list_filter = ("role", "created_at", "updated_at", "thread__chat_user")
    search_fields = (
        "content",
        "system_prompt",
        "thread__title",
        "thread__chat_user__user__username",
    )
    readonly_fields = ("id", "created_at", "updated_at")
    ordering = ("created_at",)

    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content

    content_preview.short_description = _("Content Preview")
