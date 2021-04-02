import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Semaphore
from channels.db import database_sync_to_async


class SemaphoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pk_test = self.scope['url_route']['kwargs']['pk_test']
        self.room_group_name = 'semaphore_%s' % self.pk_test
        self.status = await database_sync_to_async(self.get_status)()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    def get_status(self):
        semaphores = Semaphore.objects.all()
        stat = semaphores.filter(controlUrl=self.pk_test)
        return stat


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print("New event is received")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if message == 'GREEN':
            self.status = 'Ready'

        await database_sync_to_async(self.status.save)()

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
        self.pk_test =  self.scope['url_route']['kwargs']['pk_test']
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