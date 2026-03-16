import os
from celery import Celery
from django.conf import settings
from datetime import timedelta

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Load config from Django settings, using CELERY_ namespace
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.broker_url = settings.CELERY_BROKER_URL

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()


PROJECT_HEALTH_CHECK_INTERVAL_HOURS = int(
    os.getenv("PROJECT_HEALTH_CHECK_INTERVAL_HOURS", 6)
)
PROJECT_HEALTH_CHECK_INTERVAL_MINUTES = int(
    os.getenv("PROJECT_HEALTH_CHECK_INTERVAL_MINUTES", 0)
)

app.conf.beat_schedule = {
    "run-project-health-check": {
        "task": "healthcheck.tasks.run_project_health_checks",
        "schedule": timedelta(
            hours=PROJECT_HEALTH_CHECK_INTERVAL_HOURS,
            minutes=PROJECT_HEALTH_CHECK_INTERVAL_MINUTES,
        ),
    },
    "check-server-expiry": {
        "task": "servers.check_server_expiry",
        "schedule": timedelta(minutes=2),
    },
}
