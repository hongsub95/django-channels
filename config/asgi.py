"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter,URLRouter
from django.core.asgi import get_asgi_application

from app import routing as app_routing
from chat import routing as chat_routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http":django_asgi_app,
    # 웹소켓 consumer 호출하기 전에, 쿠키,세션,인증 미들웨어가 먼저 수행
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(                
            URLRouter(
                app_routing.websocket_urlpatterns+
                chat_routing.websocket_urlpatterns
            )
        )
    ),
})
