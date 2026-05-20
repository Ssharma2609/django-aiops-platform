# 🚀 Real-Time AIOps Monitoring Platform

A full-stack real-time AIOps (Artificial Intelligence for IT Operations) platform built using Django, React, Celery, Redis, Elasticsearch, Kibana, and WebSockets.

This platform simulates modern enterprise infrastructure monitoring systems by generating live infrastructure metrics, detecting anomalies, creating incidents, streaming real-time updates, and visualizing telemetry using Kibana dashboards.

---

# 📌 Features

## ✅ Real-Time Infrastructure Monitoring

* Live CPU, Memory, Disk, and Network metric generation
* Auto-refreshing monitoring dashboard
* Real-time WebSocket metric streaming

## ✅ Anomaly Detection Engine

* Detects abnormal infrastructure behavior
* CPU spike detection
* Memory threshold monitoring
* Disk usage anomaly detection
* Network traffic spike detection

## ✅ Incident Management

* Automatic incident creation
* Incident severity categorization
* Real-time incident visualization

## ✅ Root Cause Analysis (RCA)

* AI-inspired RCA simulation
* Service-level anomaly correlation
* Infrastructure event tracing

## ✅ Elasticsearch + Kibana Observability

* Centralized metric indexing
* Real-time observability pipeline
* Kibana dashboards and analytics
* Searchable infrastructure telemetry

## ✅ Asynchronous Task Processing

* Celery workers
* Celery Beat scheduling
* Redis message broker integration

## ✅ Modern Frontend Dashboard

* React + TypeScript frontend
* Live charts using Recharts
* Real-time infrastructure analytics
* Interactive monitoring UI

## ✅ Dockerized Architecture

* Fully containerized setup
* Docker Compose orchestration
* Multi-service infrastructure deployment

---

# 🏗️ System Architecture

```text
                         ┌──────────────────┐
                         │   React Frontend │
                         │  Realtime Charts │
                         └────────┬─────────┘
                                  │
                                  ▼
                        ┌────────────────────┐
                        │ Django REST API    │
                        │ Django Channels    │
                        └────────┬───────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
      ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
      │ PostgreSQL  │    │ Redis Queue │    │ WebSockets  │
      │ Metrics DB  │    │ Celery Bus  │    │ Live Stream │
      └──────┬──────┘    └──────┬──────┘    └─────────────┘
             │                  │
             ▼                  ▼
      ┌─────────────┐    ┌─────────────┐
      │ Celery Beat │    │ Celery      │
      │ Scheduler   │    │ Workers     │
      └──────┬──────┘    └──────┬──────┘
             │                  │
             └────────┬─────────┘
                      ▼
             ┌─────────────────┐
             │ Elasticsearch   │
             │ Metrics Logs    │
             └────────┬────────┘
                      ▼
               ┌─────────────┐
               │ Kibana      │
               │ Dashboards  │
               └─────────────┘
```

---

# 🛠️ Tech Stack

## Backend

* Django
* Django REST Framework
* Django Channels
* Celery
* Redis
* PostgreSQL

## Frontend

* React
* TypeScript
* Recharts
* Axios

## Observability

* Elasticsearch
* Kibana

## Infrastructure

* Docker
* Docker Compose

---

# 📊 Screenshots

## Dashboard

Add screenshot here:

```text
docs/screenshots/dashboard.png
```

## Kibana Dashboard

Add screenshot here:

```text
docs/screenshots/kibana-dashboard.png
```

## Django Admin

Add screenshot here:

```text
docs/screenshots/django-admin.png
```

## Elasticsearch Discover

Add screenshot here:

```text
docs/screenshots/elasticsearch-data.png
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/django-aiops-platform.git

cd django-aiops-platform
```

---

## 2️⃣ Start All Services

```bash
docker compose up --build
```

---

## 3️⃣ Start Celery Worker

Open new terminal:

```bash
docker compose exec backend celery -A core worker --loglevel=info
```

---

## 4️⃣ Start Celery Beat Scheduler

Open another terminal:

```bash
docker compose exec backend celery -A core beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

# 🌐 Access URLs

| Service            | URL                         |
| ------------------ | --------------------------- |
| Frontend Dashboard | http://localhost:5173       |
| Django Backend     | http://localhost:8000       |
| Django Admin       | http://localhost:8000/admin |
| Elasticsearch      | http://localhost:9200       |
| Kibana             | http://localhost:5601       |

---

# 🔄 WebSocket Flow

The platform uses Django Channels + WebSockets for real-time metric streaming.

## Flow

```text
Celery Worker
      ↓
Metric Generation
      ↓
Database Save
      ↓
WebSocket Broadcast
      ↓
React Frontend Update
```

This enables:

* live metric updates
* real-time anomaly alerts
* dynamic dashboard refresh

---

# 📈 Elasticsearch + Kibana

Infrastructure metrics are indexed into Elasticsearch in real time.

## Indexed Fields

* hostname
* service_name
* metric_type
* metric_value
* timestamp

## Kibana Features

* live dashboards
* metric filtering
* observability analytics
* telemetry exploration
* incident trend analysis

---

# ⚡ Celery Architecture

## Celery Beat

Schedules periodic metric generation tasks.

## Celery Workers

Process asynchronous jobs including:

* metric generation
* anomaly detection
* incident creation
* Elasticsearch indexing

## Redis

Acts as the message broker between scheduler and workers.

---

# 🔥 Key Highlights

* Real-time monitoring system
* Distributed asynchronous architecture
* WebSocket-powered frontend updates
* Centralized observability stack
* Dockerized infrastructure
* ELK integration
* Production-style monitoring simulation

---

# 🚀 Future Improvements

## AI/ML Enhancements

* Isolation Forest anomaly detection
* LSTM-based forecasting
* AI-generated RCA summaries
* Predictive infrastructure alerts

## DevOps Enhancements

* Kubernetes deployment
* Helm charts
* CI/CD pipelines
* GitHub Actions integration

## Observability Enhancements

* Prometheus integration
* Grafana dashboards
* Loki log aggregation
* OpenTelemetry tracing

## Security Enhancements

* JWT authentication
* RBAC authorization
* Multi-user support

---

# 👨‍💻 Author

Developed as a real-time AIOps platform prototype for learning, experimentation, observability engineering, and modern DevOps practices.

---

# ⭐ If You Like This Project

Please consider starring the repository ⭐
