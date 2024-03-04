from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from users.models import User
from .models import ChatRoom, Message

class  ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        request_user = self.scope['user']
        print(request_user,"USER")
        if request_user:
            self.chat_with_user = self.scope['url_route']['kwargs']['id']
            user_ids = [int(request_user.id),int(self.chat_with_user)]
            user_ids = sorted(user_ids)
            self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            self.chat_room = await self.get_or_create_chat_room()
        await self.accept()
        
        
    
    @database_sync_to_async
    def get_or_create_chat_room(self):
        user1 = self.scope['user']
        user2 = User.objects.get(id=self.chat_with_user)
        user_ids = sorted([user1.id, user2.id])
        user1, user2 = User.objects.filter(id__in=user_ids)
        return ChatRoom.objects.get_or_create(user1=user1, user2=user2)
    
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data['message']
        await self.save_message(message)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message
            }
        )
        
    @database_sync_to_async
    def save_message(self, message_content):
        chat_room, _ = self.chat_room  # Extracting the ChatRoom instance from the tuple
        Message.objects.create(
        chat_room=chat_room,
        user=self.scope['user'],
        content=message_content
    )
        
    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    @database_sync_to_async
    def get_message_object(self, message_content):
        try:
            message = Message.objects.get(content=message_content)
            message_obj = {
                'id': message.id,
                'chat_room': message.chat_room.id, 
                'user': message.user.id, 
                'content': message.content,
                'timestamp': message.timestamp.isoformat(), 
            }
            return message_obj
        except Message.DoesNotExist:
            return None
        
    async def chat_message(self, event):
        message = event['message']
        message_obj = await self.get_message_object(message)
        await self.send(text_data=json.dumps(message_obj))