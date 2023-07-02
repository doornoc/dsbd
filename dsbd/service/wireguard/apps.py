from django.apps import AppConfig


class Service(AppConfig):
    name = "dsbd.service.wireguard"
    verbose_name = "Wireguard"

    def ready(self):
        from . import signals