from elasticsearch import Elasticsearch
from datetime import datetime

es = Elasticsearch("http://elasticsearch:9200")


def log_metric(metric):

    document = {
        "hostname": metric.hostname,
        "service_name": metric.service_name,
        "metric_type": metric.metric_type,
        "metric_value": metric.metric_value,
        "timestamp": datetime.utcnow(),
    }

    es.index(
        index="metrics-logs",
        document=document
    )