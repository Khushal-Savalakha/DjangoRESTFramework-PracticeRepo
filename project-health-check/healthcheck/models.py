from django.db import models
from services.models import BaseAuditModel
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class ProjectDetail(BaseAuditModel):
    project_name = models.CharField(max_length=200, unique=True)
    project_url = models.URLField()

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="projects",
        blank=True,
    )

    def __str__(self):
        return self.project_name


class ProjectHealthLog(BaseAuditModel):
    project = models.ForeignKey(
        ProjectDetail,
        on_delete=models.CASCADE,
        related_name="health_logs",
    )

    project_response = models.TextField(null=True, blank=True)
    project_status_code = models.IntegerField()

    def __str__(self):
        return f"{self.project.project_name} - {self.project_status_code}"


class ProjectNotificationLog(BaseAuditModel):
    project_health = models.ForeignKey(
        ProjectHealthLog,
        on_delete=models.CASCADE,
        related_name="email_notifications",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_notifications",
    )

    retry_count = models.IntegerField(default=0)
    notified_successfully = models.BooleanField(default=False)

    class Meta:
        unique_together = ("project_health", "user")

    def __str__(self):
        return f"{self.project_health.project.project_name} - {self.user.email}"


class ServerDetails(BaseAuditModel):
    class EnvironmentType(models.TextChoices):
        PRODUCTION = "production", _("Production")
        DEVELOPMENT = "development", _("Development")
        STAGING = "staging", _("Staging")
        OTHER = "other", _("Other")

    class OwnershipType(models.TextChoices):
        CLIENT = "client", _("Client")
        PERSONAL = "personal", _("Personal")
        ON_PREMISE = "on_premise", _("On Premise")

    class ServerStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        EXPIRED = "expired", _("Expired")
        SUSPENDED = "suspended", _("Suspended")

    name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(unique=True, db_index=True)
    description = models.TextField(blank=True)

    environment = models.CharField(
        max_length=20,
        choices=EnvironmentType.choices,
        default=EnvironmentType.DEVELOPMENT,
        db_index=True,
    )

    ownership_type = models.CharField(
        max_length=20,
        choices=OwnershipType.choices,
        default=OwnershipType.CLIENT,
        db_index=True,
    )

    status = models.CharField(
        max_length=20,
        choices=ServerStatus.choices,
        default=ServerStatus.ACTIVE,
        db_index=True,
    )

    purchased_on = models.DateField(null=True, blank=True)
    expires_on = models.DateField(null=True, blank=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="monitored_servers",
        blank=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["environment"]),
            models.Index(fields=["ownership_type"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class ServerMonitoringConfig(BaseAuditModel):
    server = models.OneToOneField(
        ServerDetails,
        on_delete=models.CASCADE,
        related_name="monitoring_config",
    )

    cpu_threshold_percent = models.FloatField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    memory_threshold_percent = models.FloatField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    disk_threshold_percent = models.FloatField(
        default=85,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    def __str__(self):
        return f"{self.server.ip_address} - {self.server.name}"


class ServerHealthLog(BaseAuditModel):
    class HealthStatus(models.TextChoices):
        HEALTHY = "healthy", _("Healthy")
        WARNING = "warning", _("Warning")
        CRITICAL = "critical", _("Critical")

    server = models.ForeignKey(
        ServerDetails,
        on_delete=models.CASCADE,
        related_name="health_logs",
    )

    cpu_usage_percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    memory_usage_percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    disk_usage_percent = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    health_status = models.CharField(
        max_length=20,
        choices=HealthStatus.choices,
    )
    error_message = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["server"]),
            models.Index(fields=["health_status"]),
        ]

    def __str__(self):
        return f"{self.server.name} - {self.health_status}"


class ServerHealthNotificationLog(BaseAuditModel):
    server_health = models.ForeignKey(
        ServerHealthLog,
        on_delete=models.CASCADE,
        related_name="notifications",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="system_notifications",
    )

    retry_count = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["server_health", "user"], name="server_health_user_notification"
            )
        ]

    def __str__(self):
        return f"{self.server_health.server.ip_address} - {self.user.email}"

class ServerExpiryNotificationLog(BaseAuditModel):
    server = models.ForeignKey(
        ServerDetails,
        on_delete=models.CASCADE,
        related_name="expiry_notifications",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    remaining_days = models.IntegerField()
    expires_on = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["server", "user", "expires_on"],
                name="unique_server_expiry_notification"
            )
        ]