from django.db import models


class Incident(models.Model):

    SEVERITY_LEVELS = [
        ("LOW", "LOW"),
        ("MEDIUM", "MEDIUM"),
        ("HIGH", "HIGH"),
        ("CRITICAL", "CRITICAL"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "OPEN"),
        ("INVESTIGATING", "INVESTIGATING"),
        ("RESOLVED", "RESOLVED"),
    ]

    title = models.CharField(max_length=255)

    description = models.TextField()

    service_name = models.CharField(max_length=255)

    severity = models.CharField(
        max_length=50,
        choices=SEVERITY_LEVELS,
    )

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="OPEN",
    )

    source = models.CharField(max_length=255)

    anomaly_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return (
            f"{self.service_name} - "
            f"{self.severity}"
        )