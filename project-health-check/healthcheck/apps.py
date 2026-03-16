from django.apps import AppConfig


class HealthcheckConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "healthcheck"

    def ready(self):
        from . import signals

        _ = signals
        return super().ready()
