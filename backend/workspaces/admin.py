from django.contrib import admin

from .models import Workspace


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = (
        "workspace_name",
        "organization",
        "is_archived",
        "created_by",
        "created_at",
        "public_analytics",
    )
    list_filter = ("is_archived", "public_analytics", "organization")
    search_fields = ("workspace_name", "organization__title", "created_by__email")
    ordering = ("workspace_name",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    filter_horizontal = ("members", "managers", "frozen_users")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "workspace_name",
                    "organization",
                    "created_by",
                    "is_archived",
                    "public_analytics",
                )
            },
        ),
        ("Members", {"fields": ("members", "managers", "frozen_users")}),
        ("Timestamps", {"fields": ("created_at",), "classes": ("collapse",)}),
    )
