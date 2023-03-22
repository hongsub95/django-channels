from django.urls import path
from chat import consumer
websocket_urlpatterns=[
    path("ws/chat/<str:room_name>/chat/",consumer.ChatConsumer.as_asgi())
]