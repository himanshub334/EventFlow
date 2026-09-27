import asyncio, json
from datetime import datetime, timezone
from pymongo.errors import DuplicateKeyError
from .clients import ensure_mongo_collection, events_collection, publish_sqs
from .enrichment import enrich_context
from .models import AdEvent
from .stream import ensure_consumer_group, read_events, acknowledge

async def process_message(stream_id, fields):
    event = AdEvent.model_validate(json.loads(fields["payload"]))
    enriched = event.model_dump(mode="json")
    enriched["context"] = await enrich_context(event.campaign_id)
    enriched["processed_at"] = datetime.now(timezone.utc).isoformat()
    try:
        events_collection().insert_one(enriched)
    except DuplicateKeyError:
        pass
    publish_sqs(enriched)
    acknowledge(stream_id)

async def worker_loop():
    ensure_consumer_group()
    ensure_mongo_collection()
    while True:
        for _, messages in read_events():
            for sid, fields in messages:
                try: await process_message(sid, fields)
                except Exception as exc: print(f"processing failed {sid}: {exc}")
        await asyncio.sleep(.05)

if __name__ == "__main__":
    asyncio.run(worker_loop())
