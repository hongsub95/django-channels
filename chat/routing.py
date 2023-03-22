from django.urls import path
from chat import consumer
websocket_urlpatterns=[
    path("ws/chat/<int:room_pk>/chat/",consumer.ChatConsumer.as_asgi())
]