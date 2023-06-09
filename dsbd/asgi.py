"""
ASGI config for dsbd project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from importlib import import_module

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

from dsbd.ticket import routing
from dsbd.custom_admin import routing as custom_admin_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dsbd.settings')

url = []
url += routing.urlpatterns
url += custom_admin_routing.urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(url)
        )
    )

})
