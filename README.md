# EventFlow — Real-Time Ad Event Streaming Pipeline

Portfolio-ready Python streaming pipeline using FastAPI, Redis Streams, asyncio, MongoDB, AWS SQS/Lambda, Docker and CloudWatch-oriented monitoring.

## Architecture

```text
Ad Events -> FastAPI -> Redis Streams -> Async Worker
                                      -> Redis TTL enrichment cache
                                      -> MongoDB time-series
                                      -> SQS -> Lambda aggregation

CloudWatch / health report -> operational monitoring
SQS DLQ -> failed downstream events
```

## Run

```bash
docker compose up -d
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Swagger: http://localhost:8000/docs
Health: http://localhost:8000/health

Worker:

```bash
python -m app.worker
```

Send an event:

```bash
curl -X POST http://localhost:8000/events ^
  -H "Content-Type: application/json" ^
  -d "{"event_id":"evt-001","event_type":"impression","campaign_id":"camp-101","device_id":"device-42","timestamp":"2026-09-27T12:00:00Z","country":"IN"}"
```

## Delivery semantics

Redis Streams consumer groups provide at-least-once delivery. The worker uses deterministic event IDs plus a MongoDB unique index so persistence is idempotent on retries. This avoids incorrectly claiming global exactly-once semantics.

## Components

- FastAPI ingestion + Swagger/OpenAPI
- Redis Streams + consumer groups
- asyncio validation/enrichment worker
- Redis TTL contextual metadata cache
- MongoDB time-series collection + TTL retention
- SQS + DLQ via LocalStack
- AWS Lambda aggregation handler
- CloudWatch dashboard/alarm examples
- Daily health-report script
- pytest tests
- Docker Compose
- GitHub Actions CI/CD skeleton

## GitHub

```bash
git init
git add .
git commit -m "Initial commit - EventFlow real-time ad event pipeline"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/eventflow.git
git push -u origin main
```

The repository includes reproducible monitoring and load-test notes. Do not claim a specific cache reduction or throughput number until you run and measure it.
# EventFlow
