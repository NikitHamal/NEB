"""
NEBians ASGI entry point.

Routes HTTP traffic to the standard Django WSGI stack and WebSocket traffic
to Channels consumers. Channels is configured with a Redis layer so the
daphne process can fan out events to workers across Passenger processes.

Run with:
    daphne -b 127.0.0.1 -p 8001 nebians.asgi:application

Passenger continues to serve normal HTTP/HTTPS traffic on port 80/443 via
nebians.wsgi:application (configured by the cPanel Python Selector).
WebSocket traffic is reverse-proxied through a Cloudflare tunnel to the
local daphne listener on 127.0.0.1:8001.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nebians.settings')
django.setup()

# Import these AFTER django.setup() so app registry is ready
from channels.routing import ProtocolTypeRouter, URLRouter  # noqa: E402
from channels.auth import AuthMiddlewareStack  # noqa: E402
from django.core.asgi import get_asgi_application  # noqa: E402

from api.middleware_ws import OriginValidatorMiddleware, JWTAuthMiddleware  # noqa: E402
from api.routing_ws import websocket_urlpatterns  # noqa: E402


# HTTP traffic still goes through Django (Passenger also calls this stack
# when a request is dispatched to the WSGI app, so it's a no-op there).
http_app = get_asgi_application()


# scope['user'] to the resolved User, or AnonymousUser.
websocket_stack = OriginValidatorMiddleware(
    AuthMiddlewareStack(
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    )
)


application = ProtocolTypeRouter({
    'http': http_app,
    'websocket': websocket_stack,
})
