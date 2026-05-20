from django.db import models


class Metric(models.Model):

    METRIC_TYPES = [
        ("CPU", "CPU"),
        ("MEMORY", "MEMORY"),
        ("DISK", "DISK"),
        ("NETWORK", "NETWORK"),
    ]

    hostname = models.CharField(max_length=100)

    service_name = models.CharField(max_length=100)

    metric_type = models.CharField(
        max_length=50,
        choices=METRIC_TYPES
    )

    metric_value = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"{self.hostname} - "
            f"{self.metric_type} - "
            f"{self.metric_value}"
        )


class Anomaly(models.Model):

    SEVERITY_LEVELS = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
        ("CRITICAL", "CRITICAL"),
    ]

    hostname = models.CharField(max_length=100)

    service_name = models.CharField(max_length=100)

    metric_type = models.CharField(max_length=50)

    metric_value = models.FloatField()

    severity = models.CharField(
        max_length=50,
        choices=SEVERITY_LEVELS
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"{self.hostname} - "
            f"{self.metric_type} - "
            f"{self.severity}"
        )

class RCAnalysis(models.Model):

    anomaly = models.ForeignKey(
        Anomaly,
        on_delete=models.CASCADE
    )

    probable_cause = models.TextField()

    impacted_service = models.CharField(max_length=255)

    confidence_score = models.FloatField()

    recommendation = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"RCA - "
            f"{self.impacted_service} - "
            f"{self.confidence_score}"
        )        