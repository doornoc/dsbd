from django.apps import AppConfig


class Ticket(AppConfig):
    name = "dsbd.ticket"
    verbose_name = "チケット"

    def ready(self):
        from . import signals
