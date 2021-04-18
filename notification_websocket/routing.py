from django.urls import path

from notification_websocket.notification_consumer import TimelineConsumer

websocket_urlpatterns = [
    path('ws/timeline/',  TimelineConsumer.as_asgi()),
]
