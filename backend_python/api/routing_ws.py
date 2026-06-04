"""
WebSocket URL routing for NEBians.

Single endpoint /ws/ that handles all real-time traffic. The consumer
inside resolves subscription channels from incoming messages.
"""
from django.urls import re_path

from . import consumers_ws

websocket_urlpatterns = [
    # Match /ws/ and /ws (with or without trailing slash).
    re_path(r'^ws/?$', consumers_ws.RealtimeConsumer.as_asgi()),
]
