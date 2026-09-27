import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    mongo_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongo_db: str = os.getenv("MONGODB_DB", "eventflow")
    stream: str = os.getenv("REDIS_STREAM", "ad-events")
    group: str = os.getenv("REDIS_GROUP", "eventflow-workers")
    consumer: str = os.getenv("REDIS_CONSUMER", "worker-1")
    retention_seconds: int = int(os.getenv("MONGODB_RETENTION_SECONDS", "2592000"))
    context_api_url: str = os.getenv("CONTEXT_API_URL", "http://localhost:8000/mock/context")
    context_cache_ttl: int = int(os.getenv("CONTEXT_CACHE_TTL", "300"))
    aws_endpoint_url: str | None = os.getenv("AWS_ENDPOINT_URL")
    aws_region: str = os.getenv("AWS_REGION", "ap-south-1")
    sqs_queue_url: str = os.getenv("SQS_QUEUE_URL", "http://localhost:4566/000000000000/eventflow-events")

settings = Settings()
