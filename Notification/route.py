
from django.urls import path
from .Consumers import NotificationConsumer

notification_websocket_urlpatterns = [
    path('ws/notifications/<int:id>/', NotificationConsumer.as_asgi()),
]