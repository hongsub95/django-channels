"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application

from app import routing as app_routing
from chat import routing as chat_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http":django_asgi_app,
    "websocket":URLRouter(
        app_routing.websocket_urlpatterns+
        chat_routing.websocket_urlpatterns
    )
})
