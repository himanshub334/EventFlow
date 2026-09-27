from fastapi import FastAPI
from .models import AdEvent
from .stream import publish_event, ensure_consumer_group, pending_count
from .clients import redis_client, mongo_client

app = FastAPI(title="EventFlow", version="1.0.0", description="Real-time ad event ingestion pipeline")

@app.on_event("startup")
def startup(): ensure_consumer_group()

@app.get("/health")
def health():
    redis_client.ping()
    mongo_client.admin.command("ping")
    return {"status":"UP","redis":"UP","mongodb":"UP","consumer_pending":pending_count()}

@app.post("/events", status_code=202)
def ingest(event: AdEvent):
    sid = publish_event(event.model_dump(mode="json"))
    return {"accepted":True,"event_id":event.event_id,"stream_id":sid}

@app.get("/mock/context")
def mock_context(campaign_id: str):
    return {"campaign_id":campaign_id,"content_category":"sports","device_type":"connected_tv","publisher_tier":"premium"}
