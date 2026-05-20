import asyncio
import random
import time

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer

from django.core.management.base import BaseCommand

from apps.monitoring.models import Metric


class Command(BaseCommand):

    help = "Generate synthetic infrastructure metrics"

    SERVICES = [
        "payment-service",
        "recommendation-engine",
        "postgres-db",
        "auth-service",
        "notification-service",
    ]

    HOSTS = [
        "node-1",
        "node-2",
        "node-3",
        "node-4",
    ]

    METRIC_TYPES = [
        "CPU",
        "MEMORY",
        "DISK",
        "NETWORK",
    ]

    def handle(self, *args, **kwargs):

        channel_layer = (
            get_channel_layer()
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Starting metric generator..."
            )
        )

        while True:

            metric = Metric.objects.create(

                hostname=random.choice(
                    self.HOSTS
                ),

                service_name=random.choice(
                    self.SERVICES
                ),

                metric_type=random.choice(
                    self.METRIC_TYPES
                ),

                metric_value=round(
                    random.uniform(10, 100),
                    2
                )
            )
            is_anomaly = False

            if (
                metric.metric_type == "CPU"
                and metric.metric_value > 85
            ):
                is_anomaly = True

            elif (
                metric.metric_type == "MEMORY"
                and metric.metric_value > 90
            ):
                is_anomaly = True

            elif (
                metric.metric_type == "DISK"
                and metric.metric_value > 80
            ):
                is_anomaly = True

            elif (
                metric.metric_type == "NETWORK"
                and metric.metric_value > 95
            ):
                is_anomaly = True


            metric_payload = {

                "hostname":
                    metric.hostname,

                "service_name":
                    metric.service_name,

                "metric_type":
                    metric.metric_type,

                "metric_value":
                    metric.metric_value,

                "is_anomaly":
                    is_anomaly,

            }

            async_to_sync(
                channel_layer.group_send
            )(

                "metrics",

                {
                    "type":
                        "send_metric",

                    "message":
                        metric_payload
                }

            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Broadcasted: "
                    f"{metric.metric_type} | "
                    f"{metric.metric_value}"
                )
            )

            time.sleep(2)