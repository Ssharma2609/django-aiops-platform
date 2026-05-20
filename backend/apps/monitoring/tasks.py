from celery import shared_task

from apps.incidents.models import Incident
from apps.monitoring.models import (Metric,Anomaly,RCAnalysis,)

from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from .logger import log_metric

import random


SERVICES = [
    "payment-service",
    "auth-service",
    "recommendation-engine",
    "postgres-db",
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


def generate_rca(anomaly):

    probable_causes = {
        "CPU": [
            "High application traffic",
            "Container resource exhaustion",
            "Infinite processing loop",
        ],

        "MEMORY": [
            "Memory leak detected",
            "Excessive caching",
            "Database memory pressure",
        ],

        "DISK": [
            "Disk saturation",
            "Log storage overflow",
            "High I/O operations",
        ],

        "NETWORK": [
            "Packet loss detected",
            "Network congestion",
            "Service communication failure",
        ],
    }

    recommendations = {
        "CPU": [
            "Scale Kubernetes deployment",
            "Increase CPU resource limits",
            "Restart overloaded service",
        ],

        "MEMORY": [
            "Restart affected containers",
            "Increase memory allocation",
            "Investigate memory leak",
        ],

        "DISK": [
            "Clean old logs",
            "Expand storage volume",
            "Optimize disk usage",
        ],

        "NETWORK": [
            "Inspect network routes",
            "Restart ingress controller",
            "Scale network infrastructure",
        ],
    }

    probable_cause = random.choice(
        probable_causes[anomaly.metric_type]
    )

    recommendation = random.choice(
        recommendations[anomaly.metric_type]
    )

    confidence_score = round(
        random.uniform(75, 99),
        2
    )

    RCAnalysis.objects.create(
        anomaly=anomaly,
        probable_cause=probable_cause,
        impacted_service=anomaly.service_name,
        confidence_score=confidence_score,
        recommendation=recommendation,
    )

    print(
        f"RCA GENERATED: "
        f"{probable_cause}"
    )

def correlate_incident(anomaly):

    existing_incident = Incident.objects.filter(
        service_name=anomaly.service_name,
        status="OPEN",
    ).first()

    if existing_incident:

        existing_incident.anomaly_count += 1

        existing_incident.save()

        print(
            f"INCIDENT UPDATED: "
            f"{existing_incident.service_name}"
        )

    else:

        Incident.objects.create(
            title=f"{anomaly.service_name} degradation",
            description=(
                f"Multiple anomalies detected "
                f"for {anomaly.service_name}"
            ),
            service_name=anomaly.service_name,
            severity=anomaly.severity,
            status="OPEN",
            source="AI Correlation Engine",
            anomaly_count=1,
        )

        print(
            f"NEW INCIDENT CREATED: "
            f"{anomaly.service_name}"
        )

def detect_anomaly(metric):

    value = metric.metric_value

    severity = None

    if value >= 70:
        severity = "HIGH"

    if value >= 90:
        severity = "CRITICAL"

    if severity:

        anomaly = Anomaly.objects.create(
            hostname=metric.hostname,
            service_name=metric.service_name,
            metric_type=metric.metric_type,
            metric_value=metric.metric_value,
            severity=severity,
            message=f"{metric.metric_type} anomaly detected",
        )

        print(
            f"ANOMALY DETECTED: "
            f"{metric.hostname}"
        )

        generate_rca(anomaly)


        correlate_incident(anomaly)


@shared_task
def generate_metric_task():
    
    print("TASK EXECUTED")
    print("GENERATING METRICS...")

    for _ in range(10):

        metric = Metric.objects.create(
            hostname=random.choice(HOSTS),
            service_name=random.choice(SERVICES),
            metric_type=random.choice(METRIC_TYPES),
            metric_value=round(random.uniform(10, 100), 2),
        )
        
        log_metric(metric)
        channel_layer = get_channel_layer()

        async_to_sync(
            channel_layer.group_send
        )(
            "metrics_room",
            {
                "type": "send_metrics",
                "data": {
                    "hostname": metric.hostname,
                    "service_name": metric.service_name,
                    "metric_type": metric.metric_type,
                    "metric_value": metric.metric_value,
                }
            }
        )

        

        detect_anomaly(metric)

    print("METRICS GENERATED SUCCESSFULLY")