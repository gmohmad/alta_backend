from django.apps import AppConfig


class PatternsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.patterns'

    def ready(self) -> None:
        import api.patterns.signals
