"""
WebSocket routing for chat app.
Defines WebSocket URL patterns.
"""
from django.urls import re_path
from . import consumers

# WebSocket URL patterns
# ws/rooms/<room_code>/ connects to the RoomConsumer
websocket_urlpatterns = [
    re_path(r'ws/rooms/(?P<room_code>\w+)/$', consumers.RoomConsumer.as_asgi()),
]
