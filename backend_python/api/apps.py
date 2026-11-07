"""
Django app config for the api app.
"""
from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        from api import search_signals  # noqa: F401 — register Meilisearch sync signals
        from api import signals
        signals.register_hooks()
        from api import resource_alerts
        resource_alerts.register_hooks()
