from channels.consumer import SyncConsumer, AsyncConsumer
# from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
# from .models import UserChat, GroupChat
from channels.db import database_sync_to_async


class MySyncConsumer(SyncConsumer):

    def websocket_connect(self, event):
        print("Web socket connect", event)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Message receive", event)
        print(f"Message {event['text']}")
        for i in range(10):
            self.send({
                'type': 'websocket.send',
                'text': f'Message send to client from message from Async times : {str(i)}'
            })
            sleep(1)

    def websocket_disconnect(self, event):
        print("WebSocket disconnect!", event)
        # raise StopConsumer()


class ASyncConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("Web socket connect", event)
        print('Channel layer', self.channel_layer)
        print('Channel name', self.channel_name)
        print('Get dynamic group name', self.scope['url_route']['kwargs']['group_name'])
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("Message receive", event)
        data = json.loads(event['text'])
        # group_name = await database_sync_to_async(GroupChat.objects.get)(group_name=self.group_name)
        # user_chat = UserChat(
        #     messgaes=data['msg'],
        #     group_name_id=group_name.id
        # )
        # await database_sync_to_async(user_chat.save)()
        # for i in range(2):
        #     await self.send({
        #         'type': 'websocket.send',
        #         'text': f'Message send to client from message from Async times : {str(i)}'
        #     })
        #     await asyncio.sleep(1)
        await self.channel_layer.group_send(self.group_name, {
            'type': 'send_message',
            'message': event['text']
        })

    # custom handler
    async def send_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    async def websocket_disconnect(self, event):
        print("WebSocket disconnect!", event)
