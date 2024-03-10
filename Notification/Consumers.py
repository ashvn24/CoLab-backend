# consumers.py

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Notification

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'notifications_group'
        self.request_user = self.scope['url_route']['kwargs']['id']
        print('requser-------',self.request_user)
        # Join notifications group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave notifications group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def send_notification(self, event):
        notification = event['notification']
        recipient_user_id = event['recipient_user_id']

        # Check if the recipient user matches the currently connected user
        if self.request_user == recipient_user_id:
            self.send(text_data=json.dumps(notification))