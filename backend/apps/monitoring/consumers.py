import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MetricsConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_group_name = "metrics_room"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        print("WebSocket Connected")

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print("WebSocket Disconnected")

    async def send_metrics(self, event):

        await self.send(
            text_data=json.dumps(event["data"])
        )