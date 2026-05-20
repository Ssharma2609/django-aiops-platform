import json

from channels.generic.websocket import (
    AsyncWebsocketConsumer
)


class MetricConsumer(
    AsyncWebsocketConsumer
):

    async def connect(self):

        self.room_group_name = (
            "metrics"
        )

        await self.channel_layer.group_add(

            self.room_group_name,

            self.channel_name

        )

        await self.accept()

    async def disconnect(
        self,
        close_code
    ):

        await self.channel_layer.group_discard(

            self.room_group_name,

            self.channel_name

        )

    async def send_metric(
        self,
        event
    ):

        metric_data = event["message"]

        await self.send(
            text_data=json.dumps(
                metric_data
            )
        )