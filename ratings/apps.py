from django.apps import AppConfig


class RatingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ratings'

    def ready(self):
        import ratings.signals  # Import the signals to ensure they are registered
