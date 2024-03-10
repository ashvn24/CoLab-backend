# tests.py

from channels.testing import WebsocketCommunicator
from channels.layers import get_channel_layer
from django.test import TestCase
from .Consumers import NotificationConsumer
import asyncio

class NotificationConsumerTests(TestCase):
    async def test_notification_consumer(self):
        communicator = WebsocketCommunicator(NotificationConsumer, "/ws/notifications/")
        connected, _ = await communicator.connect()

        # Check if the WebSocket connection is established
        assert connected

        # Send a notification event to the consumer
        notification_event = {
            'type': 'send_notification',
            'notification': {
                'id': 1,
                'message': 'Test message'
            }
        }
        await communicator.send_json_to(notification_event)

        # Receive the notification from the consumer
        response = await communicator.receive_json_from()

        # Check if the notification received matches the sent notification
        assert response == notification_event['notification']

        # Disconnect the WebSocket
        await communicator.disconnect()
