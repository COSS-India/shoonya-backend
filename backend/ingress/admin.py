from django.contrib import admin

from .models import Crawler, CrawledRun


@admin.register(Crawler)
class CrawlerAdmin(admin.ModelAdmin):
    list_display = ("name", "root_url")
    search_fields = ("name", "root_url")
    readonly_fields = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "root_url", "script")}),
        ("Configuration", {"fields": ("configuration",)}),
    )


@admin.register(CrawledRun)
class CrawledRunAdmin(admin.ModelAdmin):
    list_display = ("id", "crawler")
    list_filter = ("crawler",)
    search_fields = ("crawler__name",)
    ordering = ("-id",)
    readonly_fields = ("crawler",)

    fieldsets = (
        (None, {"fields": ("crawler",)}),
        ("Metadata", {"fields": ("metadata",)}),
    )
