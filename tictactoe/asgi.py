import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from game.consumers import GameConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tictactoe.settings")

django_asgi_app = get_asgi_application()

websocket_urlpatterns = [
    path('ws/game/<int:id>/<str:name>', GameConsumer.as_asgi())
]

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    }
)