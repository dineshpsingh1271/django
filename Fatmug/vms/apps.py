from django.apps import AppConfig


class VmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vms"
    def ready(self):
        import vms.signals  # This connects your signals when the app is ready