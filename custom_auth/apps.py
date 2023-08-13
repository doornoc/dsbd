from django.apps import AppConfig


class CustomUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_auth'
    verbose_name = 'ユーザとグループ'

    def ready(self):
        from . import signals
