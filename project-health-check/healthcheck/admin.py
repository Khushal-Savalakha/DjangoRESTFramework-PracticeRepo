from django.contrib import admin
from .models import (
    ProjectDetail,
    ProjectHealthLog,
    ProjectNotificationLog,
    ServerHealthLog,
    ServerDetails,
    ServerMonitoringConfig,
    ServerHealthNotificationLog,
    ServerExpiryNotificationLog,
)


# ─────────────────────────────────────────────
#  Project
# ─────────────────────────────────────────────

@admin.register(ProjectDetail)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "project_name", "project_url", "get_users", "created_at", "updated_at"]
    search_fields = ["project_name", "project_url", "users__first_name", "users__email"]
    list_filter = ["created_at"]
    ordering = ["-created_at"]
    exclude = ["deleted_at"]

    def get_users(self, obj):
        return ", ".join([user.first_name for user in obj.users.all()])

    get_users.short_description = "Users"


# ─────────────────────────────────────────────
#  Project Health Log
# ─────────────────────────────────────────────

@admin.register(ProjectHealthLog)
class ProjectHealthLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_project_name",
        "get_project_url",
        "project_response",
        "project_status_code",
        "created_at",
    ]
    search_fields = [
        "project__project_name",
        "project__project_url",
        "project_status_code",
    ]
    list_filter = ["project_status_code", "created_at"]
    ordering = ["-created_at"]
    exclude = ["deleted_at", "updated_at"]

    def get_project_name(self, obj):
        return obj.project.project_name

    def get_project_url(self, obj):
        return obj.project.project_url

    get_project_name.short_description = "Project"
    get_project_url.short_description = "URL"


# ─────────────────────────────────────────────
#  Project Notification Log
# ─────────────────────────────────────────────

@admin.register(ProjectNotificationLog)
class ProjectNotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_project_name",
        "get_project_url",
        "user",
        "get_project_status_code",
        "get_project_response",
        "created_at",
    ]
    search_fields = [
        "project_health__project__project_name",
        "project_health__project__project_url",
        "project_health__project_status_code",
        "user__first_name",
        "user__email",
    ]
    list_filter = [
        "project_health__project_status_code",
        "created_at",
    ]
    ordering = ["-created_at"]
    exclude = ["deleted_at", "updated_at"]

    def get_project_name(self, obj):
        return obj.project_health.project.project_name

    def get_project_url(self, obj):
        return obj.project_health.project.project_url

    def get_project_response(self, obj):
        return obj.project_health.project_response

    def get_project_status_code(self, obj):
        return obj.project_health.project_status_code

    get_project_name.short_description = "Project"
    get_project_url.short_description = "URL"
    get_project_response.short_description = "Response"
    get_project_status_code.short_description = "Status Code"


# ─────────────────────────────────────────────
#  Server Details
# ─────────────────────────────────────────────

@admin.register(ServerDetails)
class ServerDetailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "ip_address",
        "environment",
        "ownership_type",
        "status",
        "purchased_on",
        "expires_on",
        "get_users",
    ]
    search_fields = ["name", "ip_address", "users__first_name", "users__email"]
    list_filter = ["environment", "ownership_type", "status"]
    ordering = ["name"]
    fields = [
        "name",
        "ip_address",
        "description",
        "environment",
        "ownership_type",
        "status",
        "purchased_on",
        "expires_on",
        "users",
    ]

    def get_users(self, obj):
        return ", ".join([user.first_name for user in obj.users.all()])

    get_users.short_description = "Users"


# ─────────────────────────────────────────────
#  Server Health Log
# ─────────────────────────────────────────────

@admin.register(ServerHealthLog)
class ServerHealthLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_ip_address",
        "cpu_usage_percent",
        "memory_usage_percent",
        "disk_usage_percent",
        "health_status",
        "error_message",
        "created_at",
    ]
    search_fields = ["server__ip_address", "server__name", "health_status"]
    list_filter = ["health_status", "created_at"]
    ordering = ["-created_at"]
    exclude = ["deleted_at", "updated_at","created_by","updated_by"]

    def get_ip_address(self, obj):
        return obj.server.ip_address

    get_ip_address.short_description = "IP Address"


# ─────────────────────────────────────────────
#  Server Monitoring Config
# ─────────────────────────────────────────────

@admin.register(ServerMonitoringConfig)
class ServerMonitoringConfigAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "server",
        "get_ip_address",
        "cpu_threshold_percent",
        "memory_threshold_percent",
        "disk_threshold_percent",
        "created_at",
    ]
    search_fields = ["server__name", "server__ip_address"]
    list_filter = ["created_at"]
    ordering = ["server__name"]
    exclude = ["deleted_at", "updated_at"]

    def get_ip_address(self, obj):
        return obj.server.ip_address

    get_ip_address.short_description = "IP Address"


# ─────────────────────────────────────────────
#  Server Health Notification Log
# ─────────────────────────────────────────────

@admin.register(ServerHealthNotificationLog)
class ServerHealthNotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_ip_address",
        "get_server_name",
        "user",
        "get_health_status",
        "retry_count",
    ]
    search_fields = [
        "server_health__server__ip_address",
        "server_health__server__name",
        "user__first_name",
        "user__email",
    ]
    list_filter = ["server_health__health_status", "retry_count"]
    ordering = ["-server_health__created_at"]
    exclude = ["deleted_at", "updated_at"]

    def get_ip_address(self, obj):
        return obj.server_health.server.ip_address

    def get_server_name(self, obj):
        return obj.server_health.server.name

    def get_health_status(self, obj):
        return obj.server_health.health_status

    get_ip_address.short_description = "IP Address"
    get_server_name.short_description = "Server"
    get_health_status.short_description = "Health Status"


# ─────────────────────────────────────────────
#  Server Expiry Notification Log
# ─────────────────────────────────────────────

@admin.register(ServerExpiryNotificationLog)
class ServerExpiryNotificationLogAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "server",
        "get_ip_address",
        "user",
        "remaining_days",
        "expires_on",
    ]
    search_fields = [
        "server__name",
        "server__ip_address",
        "user__first_name",
        "user__email",
    ]
    list_filter = ["expires_on", "server__environment", "server__status"]
    ordering = ["expires_on"]
    exclude = ["deleted_at", "updated_at", "created_by", "updated_by"]

    def get_ip_address(self, obj):
        return obj.server.ip_address

    get_ip_address.short_description = "IP Address"


# ─────────────────────────────────────────────
#  Unregister SimpleJWT token models
# ─────────────────────────────────────────────

try:
    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
    admin.site.unregister(OutstandingToken)
    admin.site.unregister(BlacklistedToken)
except Exception:
    pass