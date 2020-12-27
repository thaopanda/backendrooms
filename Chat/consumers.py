import asyncio
import json
from Account.models import MyUser
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from Chat.models import Thread, ChatMessage

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        other_user = self.scope['url_route']['kwargs']['receiver_username']
        email = self.scope['url_route']['kwargs']['sender_username']
        user = await self.get_sender(email)
        self.sender = user
        other_user = await self.get_receiver(other_user)

        print(other_user.username)
        print (user.username)
        
        thread_obj = await self.get_thread(user, other_user.username)
        self.thread_obj = thread_obj

        chat_room = f'{thread_obj.id}'
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
            await self.create_new_message(front_text)
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type":"chat_message",
                    "text":front_text
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
    def get_sender(self, username):
        return MyUser.objects.get(username=username)

    @database_sync_to_async
    def get_receiver(self, username):
        return MyUser.objects.get(username=username)

    @database_sync_to_async
    def create_new_message(self, msg):
        thread = self.thread_obj
        me = self.sender
        return ChatMessage.objects.create(thread=thread, user=me, message=msg)

class AllUserChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        chat_room = f'allUser'
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
                    "text":front_text
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
    