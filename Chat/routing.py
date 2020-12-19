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
    re_path(r"^messages/(?P<sender_username>[\w.@+-]+)/(?P<receiver_username>[\w.@+-]+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"^messages/allUser/$", consumers.AllUserChatConsumer.as_asgi()),

]