import json
from datetime import datetime, timezone
import boto3
import redis
from pymongo import MongoClient
from .config import settings

redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
mongo_client = MongoClient(settings.mongo_url)
mongo_db = mongo_client[settings.mongo_db]
sqs = boto3.client("sqs", region_name=settings.aws_region, endpoint_url=settings.aws_endpoint_url)

def utc_now(): return datetime.now(timezone.utc)
def events_collection(): return mongo_db["events"]

def ensure_mongo_collection():
    try:
        if "events" not in mongo_db.list_collection_names():
            mongo_db.create_collection("events", timeseries={
                "timeField": "timestamp", "metaField": "campaign_id", "granularity": "seconds"
            }, expireAfterSeconds=settings.retention_seconds)
        events_collection().create_index("event_id", unique=True)
    except Exception:
        events_collection().create_index("event_id", unique=True)

def publish_sqs(event: dict):
    sqs.send_message(QueueUrl=settings.sqs_queue_url, MessageBody=json.dumps(event, default=str))
