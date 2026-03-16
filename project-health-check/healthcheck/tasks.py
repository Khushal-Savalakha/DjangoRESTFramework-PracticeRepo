from celery import shared_task
import logging
from .models import ProjectDetail, ProjectHealthLog , ServerDetails ,ServerExpiryNotificationLog
import requests
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from services.tasks import send_custom_email
import os

logger = logging.getLogger(__name__)


def log_project_health(project, status_code, response):

    last_log = (
        ProjectHealthLog.objects.filter(project=project).order_by("-created_at").first()
    )

    if last_log and last_log.project_status_code == 200:
        # Same status → update existing record
        last_log.project_response = response
        last_log.save(update_fields=["project_response", "updated_at"])
        return last_log

    else:
        # Status changed → create new record
        return ProjectHealthLog.objects.create(
            project=project,
            project_status_code=status_code,
            project_response=response,
        )


@shared_task(name="healthcheck.tasks.run_project_health_checks")
def check_project_health():
    logger.info("Starting project health check task")

    projects = ProjectDetail.objects.all()

    for project in projects:
        try:
            response = requests.get(
                project.project_url,
                timeout=10,
            )

            status_code = response.status_code
            response_text = response.text if status_code != 200 else "OK"

        except requests.RequestException as e:
            status_code = 0
            response_text = str(e)

        # Use the smart logging logic
        log_project_health(
            project=project, status_code=status_code, response=response_text
        )

        logger.info(
            f"Health check completed for {project.project_name} "
            f"with status {status_code}"
        )

    logger.info("Project health check task finished")


""" 
This version of the health check task stores an individual log entry
for every health check execution.
"""
# @shared_task(name="healthcheck.tasks.run_project_health_checks")
# def check_project_health():
#     logger.info("Starting project health check task")

#     projects = ProjectDetail.objects.all()

#     for project in projects:
#         try:
#             response = requests.get(
#                 project.project_url,
#                 timeout=10,  # prevent hanging
#             )

#             status_code = response.status_code
#             if status_code != 200:
#                 response_text = response.text
#             else:
#                 response_text = "OK"

#         except requests.RequestException as e:
#             # Network error, timeout, DNS failure, etc.
#             status_code = 0
#             response_text = str(e)

#         # Save log
#         ProjectHealthLog.objects.create(
#             project=project,
#             project_status_code=status_code,
#             project_response=response_text,
#         )

#         logger.info(
#             f"Health check completed for {project.project_name} "
#             f"with status {status_code}"
#         )

#     logger.info("Project health check task finished")

SERVER_EXPIRY_ALERT_DAYS = int(os.getenv("SERVER_EXPIRY_ALERT_DAYS", 5))

@shared_task(name="servers.check_server_expiry")
def server_expiry_check():

    today = timezone.now().date()
    expiry_limit = today + timedelta(days=SERVER_EXPIRY_ALERT_DAYS)

    servers = ServerDetails.objects.filter(
        expires_on__isnull=False,
        expires_on__lte=expiry_limit,
        status=ServerDetails.ServerStatus.ACTIVE,
    ).prefetch_related("users")

    for server in servers:
        remaining_days = (server.expires_on - today).days

        for user in server.users.all():

            ServerExpiryNotificationLog.objects.get_or_create(
                server=server,
                user=user,
                expires_on=server.expires_on,
                defaults={"remaining_days": remaining_days},
            )

    logger.info("Server expiry check completed")