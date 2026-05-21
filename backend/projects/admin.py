from django.contrib import admin

from .models import Project, ProjectTaskRequestLock


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project_type",
        "project_mode",
        "project_stage",
        "src_language",
        "tgt_language",
        "organization_id",
        "workspace_id",
        "is_published",
        "is_archived",
        "created_by",
        "created_at",
    )
    list_filter = (
        "project_type",
        "project_mode",
        "project_stage",
        "is_published",
        "is_archived",
        "sampling_mode",
        "src_language",
        "tgt_language",
        "organization_id",
        "workspace_id",
    )
    search_fields = ("title", "description", "created_by__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    list_per_page = 25
    filter_horizontal = (
        "annotators",
        "annotation_reviewers",
        "review_supercheckers",
        "frozen_users",
        "dataset_id",
    )

    fieldsets = (
        (
            "Overview",
            {
                "fields": (
                    "title",
                    "description",
                    "project_type",
                    "project_mode",
                    "project_stage",
                    "color",
                    "created_by",
                    "created_at",
                    "published_at",
                    "is_published",
                    "is_archived",
                )
            },
        ),
        (
            "Scope",
            {
                "fields": (
                    "organization_id",
                    "workspace_id",
                    "src_language",
                    "tgt_language",
                )
            },
        ),
        (
            "Dataset",
            {"fields": ("dataset_id", "filter_string", "sampling_mode", "sampling_parameters_json")},
        ),
        (
            "Team",
            {
                "fields": (
                    "annotators",
                    "annotation_reviewers",
                    "review_supercheckers",
                    "frozen_users",
                )
            },
        ),
        (
            "Task Settings",
            {
                "fields": (
                    "required_annotators_per_task",
                    "tasks_pull_count_per_batch",
                    "max_pending_tasks_per_user",
                    "k_value",
                    "revision_loop_count",
                )
            },
        ),
        (
            "UI",
            {
                "fields": (
                    "show_instruction",
                    "show_skip_button",
                    "show_predictions_to_annotator",
                    "expert_instruction",
                    "label_config",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Advanced",
            {
                "fields": ("data_type", "variable_parameters", "metadata_json"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(ProjectTaskRequestLock)
class ProjectTaskRequestLockAdmin(admin.ModelAdmin):
    list_display = ("project", "user", "lock_context", "expires_at")
    list_filter = ("lock_context",)
    search_fields = ("project__title", "user__email")
    ordering = ("expires_at",)
    readonly_fields = ("project", "user", "lock_context", "expires_at")
