from django.conf.urls import url
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

# from Chat.consumers import ChatConsumer

# application = ProtocolTypeRouter({
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter(
#                 [
#                     url(r"^messages/(?P<username>[\w.@+-]+)/$", ChatConsumer)
#                 ]
#             )
#         )
#     )
# })

from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"^messages/(?P<username>[\w.@+-]+)/(?P<email>[\w.@+-]+)/$", consumers.ChatConsumer.as_asgi()),
]