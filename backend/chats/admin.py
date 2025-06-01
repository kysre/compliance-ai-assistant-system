from django.contrib import admin

from .models import ChatUser


@admin.register(ChatUser)
class ChatUserAdmin(admin.ModelAdmin):
    list_display = ("user", "user_email", "user_first_name", "user_last_name")
    list_filter = ("user__is_active", "user__date_joined")
    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    readonly_fields = ("user",)

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = "Email"

    def user_first_name(self, obj):
        return obj.user.first_name

    user_first_name.short_description = "First Name"

    def user_last_name(self, obj):
        return obj.user.last_name

    user_last_name.short_description = "Last Name"
