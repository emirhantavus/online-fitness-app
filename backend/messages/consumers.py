from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_text = data.get('message_text')
            sender_id = data.get('sender')
            receiver_id = data.get('receiver')

            if not all([message_text, sender_id, receiver_id]):
                await self.send(text_data=json.dumps({"error": "Invalid data"}))
                return

            message = await self.save_message(sender_id, receiver_id, message_text)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'id': message.id,
                    'message_text': message.message_text,
                    'sender': sender_id,
                    'receiver': receiver_id,
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({"error": str(e)}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message_text):
        User = get_user_model()
        sender = User.objects.get(pk=sender_id)
        receiver = User.objects.get(pk=receiver_id)
        return Message.objects.create(sender=sender, receiver=receiver, message_text=message_text)
