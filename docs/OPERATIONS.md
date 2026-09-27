# Operations Runbook

## Consumer lag
Check the Redis consumer-group pending count. Example alarm threshold: 1,000 unprocessed events.

Investigate worker health, external enrichment latency, Redis, MongoDB and SQS.

## Failed events
Use the SQS dead-letter queue for messages that repeatedly fail. Reprocessing must remain idempotent.

## Daily health report
Run:
```bash
python monitoring/health_report.py
```

## Context caching
Cache keys use:
```text
context:<campaign_id>
```
TTL is controlled by `CONTEXT_CACHE_TTL`.
