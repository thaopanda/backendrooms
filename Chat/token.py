from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from Account.models import MyUser


@database_sync_to_async
def get_user(email):
    try:
        return MyUser.objects.get(email=email)
    except MyUser.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware:
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        # Store the ASGI application we were passed
        self.inner = inner

    def __call__(self, scope):

        return TokenAuthMiddlewareInstance(scope, self)

class TokenAuthMiddlewareInstance:
    """
    Inner class that is instantiated once per scope.
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        # headers = dict(self.scope['headers'])

        # token_name, token_key = headers[b'sec-websocket-protocol'].decode().split(', ')
        print(self.scope['path'].split('/')[3])
        email = self.scope['path'].split('/')[3]
        
        if email is not None:
            self.scope['user'] = await get_user(email)

        else:
            self.scope['user'] = AnonymousUser()

        # Instantiate our inner application
        inner = self.inner(receive, send)

        return await inner(receive, send)