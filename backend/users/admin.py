from django.contrib.auth.models import Group
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

from .models import User
from organizations.models import Organization, Invite


class UserResource(resources.ModelResource):
    class Meta:
        import_id_fields = ("id",)
        model = User


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin):
    resource_class = UserResource

    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "organization",
        "participation_type",
        "availability_status",
        "is_active",
        "is_staff",
        "has_accepted_invite",
        "is_approved",
        "date_joined",
        "activity_at",
    )
    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_approved",
        "has_accepted_invite",
        "enable_mail",
        "participation_type",
        "availability_status",
        "organization",
    )
    search_fields = ("email", "first_name", "last_name", "username", "phone")
    ordering = ("email",)
    date_hierarchy = "date_joined"
    list_per_page = 25
    readonly_fields = ("date_joined", "activity_at")

    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "phone",
                    "profile_photo",
                )
            },
        ),
        (
            "Role & Organisation",
            {
                "fields": (
                    "role",
                    "organization",
                    "participation_type",
                    "availability_status",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_approved",
                    "has_accepted_invite",
                    "enable_mail",
                    "prefer_cl_ui",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Languages",
            {"fields": ("languages",)},
        ),
        (
            "Notifications",
            {"fields": ("notification_limit",)},
        ),
        (
            "Timestamps",
            {"fields": ("date_joined", "activity_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("title", "email_domain_name", "is_active", "created_by", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "email_domain_name", "created_by__email")
    ordering = ("title",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    fieldsets = (
        (None, {"fields": ("title", "email_domain_name", "is_active", "created_by")}),
        ("Timestamps", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "invite_code")
    list_filter = ("organization",)
    search_fields = ("user__email", "organization__title", "invite_code")
    ordering = ("organization",)


admin.site.unregister(Group)
