from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Regulation


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ("identifier", "title", "date", "authority", "link_display")
    list_filter = ("authority", "date")
    search_fields = ("identifier", "title", "text")
    date_hierarchy = "date"

    fieldsets = (
        (None, {"fields": ("identifier", "title", "date", "authority", "link")}),
        (_("Content"), {"fields": ("text",), "classes": ("collapse",)}),
    )

    def link_display(self, obj):
        if obj.link:
            return format_html('<a href="{}" target="_blank">View Source</a>', obj.link)
        return "-"

    link_display.short_description = _("Source Link")
