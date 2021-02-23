import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SemaphoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']
        self.room_group_name = 'semaphore'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("New event is received")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'semaphore_message',
                'message': message,
            }
        )

    async def semaphore_message(self, event):
        print(event)
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))


class IndexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']
        self.room_group_name = 'semaphore'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("New event is received")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'semaphore_message',
                'message': message,
            }
        )

    async def semaphore_message(self, event):
        print(event)
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message,
        }))

    pass