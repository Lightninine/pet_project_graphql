"""
ASGI config for pet_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os  # pragma: no cover
from django.conf.urls import url  # pragma: no cover
from django.core.asgi import get_asgi_application  # pragma: no cover

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_project.settings')
django_asgi_app = get_asgi_application()  # pragma: no cover

from pet_project.schema import MyGraphqlWsConsumer
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path

from django.core.asgi import get_asgi_application  # pragma: no cover

http_routes = []  # pragma: no cover
http_routes.append(url("^", django_asgi_app))

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [path("ws/graphql/", MyGraphqlWsConsumer.as_asgi())]
            )
        ),
    }
)
