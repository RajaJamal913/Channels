import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import Notification  # Import the Notification model

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Create notification for other users (not the sender)
        sender = self.scope['user']  # Get the current user who is sending the message
        all_users = User.objects.exclude(id=sender.id)  # Exclude the sender
        for user in all_users:
            Notification.objects.create(user=user, message=f"New message from {sender.username}: {message}")

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_channel': self.channel_name  # Include the sender's channel
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        sender_channel = event['sender_channel']

        # Only send the message to others, not the sender
        if self.channel_name != sender_channel:
            await self.send(text_data=json.dumps({
                'message': message
            }))
