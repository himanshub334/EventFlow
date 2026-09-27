import json
from .clients import redis_client
from .config import settings

def ensure_consumer_group():
    try:
        redis_client.xgroup_create(settings.stream, settings.group, id="0", mkstream=True)
    except Exception as exc:
        if "BUSYGROUP" not in str(exc): raise

def publish_event(event: dict):
    return redis_client.xadd(settings.stream, {"payload": json.dumps(event, default=str)})

def read_events(count=10, block_ms=1000):
    return redis_client.xreadgroup(settings.group, settings.consumer, {settings.stream: ">"}, count=count, block=block_ms)

def acknowledge(stream_id):
    redis_client.xack(settings.stream, settings.group, stream_id)

def pending_count():
    return int(redis_client.xpending(settings.stream, settings.group)["pending"])
