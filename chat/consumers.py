import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Semaphore
from channels.db import database_sync_to_async


class SemaphoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pk_test = self.scope['url_route']['kwargs']['pk_test']
        self.room_group_name = 'semaphore_%s' % self.pk_test

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

        try:
            name = text_data_json['name']
            number = text_data_json['number']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'client_message',
                    'message': message,
                    'name': name,
                    'number': number,
                }

            )
        except:
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

    async def client_message(self, event):
        print(event)
        message = event['message']
        client = event['name']
        number = event['number']

        await self.send(text_data=json.dumps({
            'message': message,
            'name': client,
            'number': number,
        }))


class IndexConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pk_test = self.scope['url_route']['kwargs']['pk_test']
        self.room_group_name = 'semaphore_%s' % self.pk_test

        print(self.room_group_name)

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

        try:
            name = text_data_json['name']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'client_message',
                    'message': message,
                    'name': name,
                }

            )
        except:
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

    async def client_message(self, event):
        print(event)
        message = event['message']
        client = event['name']

        await self.send(text_data=json.dumps({
            'message': message,
            'name': client,
        }))

    pass
