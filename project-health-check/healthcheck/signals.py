import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    ProjectHealthLog,
    ProjectNotificationLog,
    ServerDetails,
    ServerMonitoringConfig,
    ServerHealthLog,
    ServerHealthNotificationLog,
    ServerExpiryNotificationLog
)
from services.tasks import send_custom_email

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ProjectHealthLog)
def create_email_notification_logs(sender, instance, created, **kwargs):
    """
    When a health log is created and status is NOT 200,
    create ProjectNotificationLog for all project users.
    """
    if not created:
        return

    # Only notify if project failed
    if instance.project_status_code == 200:
        return

    try:
        project = instance.project
        users = project.users.all()

        for user in users:
            ProjectNotificationLog.objects.get_or_create(
                project_health=instance,
                user=user,
            )

    except Exception as e:
        logger.error(f"Failed to create ProjectNotificationLog: {str(e)}")


@receiver(post_save, sender=ProjectNotificationLog)
def send_project_failure_email(sender, instance, created, **kwargs):
    """
    Send email when ProjectNotificationLog is created.
    """
    if not created:
        return

    try:
        project_name = instance.project_health.project.project_name
        project_url = instance.project_health.project.project_url
        status_code = instance.project_health.project_status_code

        message = f"""
        Project Name: {project_name}
        Project URL: {project_url}
        Status Code: {status_code}
        """

        # Send async email
        send_custom_email.delay(
            subject=f"🚨 Project Down Alert - {project_name}",
            message=message,
            html_message=message.replace("\n", "<br>"),
            recipient_list=[instance.user.email],
        )

        # Mark as success
        instance.notified_successfully = True
        instance.save(update_fields=["notified_successfully"])

    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        """
        NOTE:
        This try/except only handles task-queue related failures such as:
        - Redis broker being down
        - Broker connection failure
        - Celery worker not running
        - .delay() call crashing
        """
        # Increment retry count
        instance.retry_count += 1
        instance.save(update_fields=["retry_count"])


@receiver(post_save, sender=ServerDetails)
def create_monitoring_config(sender, instance, created, **kwargs):
    """
    When Server Details added it's monitoring config will be added automatically.
    """
    try:
        if not created:
            return
        monitoring_config = ServerMonitoringConfig.objects.filter(
            server__ip_address=ServerDetails.ip_address
        ).first()
        if not monitoring_config:
            ServerMonitoringConfig.objects.create(
                server=instance,
                cpu_threshold_percent=80,
                memory_threshold_percent=80,
                disk_threshold_percent=80,
            )

    except Exception as e:
        logger.error(f"Failed to create ServerMonitoringConfig: {str(e)}")


@receiver(post_save, sender=ServerHealthLog)
def create_system_health_notification_log(sender, instance, created, **kwargs):
    """
    Notifications should be triggered only when the server health condition is in a Warning or Critical state.
    """
    try:
        if not created:
            return
        health_status = instance.health_status
        if health_status in [
            ServerHealthLog.HealthStatus.CRITICAL,
            ServerHealthLog.HealthStatus.WARNING,
        ]:
            users = instance.server.users.all()
            for user in users:
                ServerHealthNotificationLog.objects.get_or_create(
                    server_health=instance,
                    user=user,
                )
    except Exception as e:
        logger.error(f"Failed to create ServerMonitoringConfig: {str(e)}")


@receiver(post_save, sender=ServerHealthNotificationLog)
def send_notification_for_server_health(sender, instance, created, **kwargs):
    try:
        if not created:
            return
        error_message = instance.server_health.error_message

        if instance.user and instance.user.email:
            send_custom_email.delay(
                subject="Server Health Alert",
                message=error_message,
                html_message=error_message.replace("\n", "<br>"),
                recipient_list=[instance.user.email],
            )
    except Exception as e:
        logger.error(f"Failed to create ServerMonitoringConfig: {str(e)}")


@receiver(post_save, sender=ServerExpiryNotificationLog)
def send_server_expiry_notification(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        server = instance.server

        message = f"""
                    Server: {server.name}
                    IP Address: {server.ip_address}

                    Expiry Date: {instance.expires_on}
                    Remaining Days: {instance.remaining_days}

                    Please renew the server before expiry.
                    """

        if instance.user and instance.user.email:
            send_custom_email.delay(
                subject="🚨 Server Expiry Alert",
                message=message,
                html_message=message.replace("\n", "<br>"),
                recipient_list=[instance.user.email],
            )

    except Exception as e:
        logger.error(f"Failed to send server expiry email: {str(e)}")