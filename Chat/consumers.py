import asyncio
import json
from Account.models import MyUser
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from Chat.models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        other_user = self.scope['url_route']['kwargs']['username']
        email = self.scope['url_route']['kwargs']['email']
        user = await self.get_sender(email)
        other_user = await self.get_receiver(other_user)

        print(other_user.username)
        print (user.username)
        
        thread_obj = await self.get_thread(user, other_user.username)

        chat_room = f'{user.username}_to_{other_user.username}'
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room, 
            self.channel_name
        )
        
        await self.send({
            "type":"websocket.accept"
        })

    async def websocket_receive(self, event):
        print('received', event)
        front_text = event.get('text', None)
        if(front_text is not None):
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "text":"Hello world"
                }
            )

    async def chat_message(self, event):
        print("message message")
        await self.send({
            "type":"websocket.send",
            "text":event["text"]
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)
    
    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]

    @database_sync_to_async
    def get_sender(self, email):
        return MyUser.objects.get(email=email)

    @database_sync_to_async
    def get_receiver(self, username):
        return MyUser.objects.get(username=username)