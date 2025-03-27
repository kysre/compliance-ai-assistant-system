from django.contrib import admin

from .models import Article, Clause, Regulation


class ClauseInline(admin.TabularInline):
    model = Clause
    extra = 1


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 1
    show_change_link = True


@admin.register(Regulation)
class RegulationAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title", "description")
    inlines = [ArticleInline]
    fieldsets = (("اطلاعات اصلی", {"fields": ("title", "description")}),)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "regulation")
    list_filter = ("regulation",)
    search_fields = ("title", "text", "regulation__title")
    inlines = [ClauseInline]
    raw_id_fields = ("regulation",)


@admin.register(Clause)
class ClauseAdmin(admin.ModelAdmin):
    list_display = ("title", "article")
    list_filter = ("article__regulation",)
    search_fields = ("title", "text", "article__title")
    raw_id_fields = ("article",)
