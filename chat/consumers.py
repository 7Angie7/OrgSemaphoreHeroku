import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import *


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

        semap = Semaphore.objects.get(controlUrl=self.pk_test)

        if message == 'GREEN':
            semap.status = 'Ready'
            semap.save()
        elif message == 'RED':
            semap.status = 'Busy'
            semap.save()
        else:
            print('Ooops ... Another message?')

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