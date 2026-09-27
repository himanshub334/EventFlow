import json
import httpx
from .clients import redis_client
from .config import settings

async def enrich_context(campaign_id: str):
    key = f"context:{campaign_id}"
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    async with httpx.AsyncClient(timeout=2) as client:
        response = await client.get(settings.context_api_url, params={"campaign_id": campaign_id})
        response.raise_for_status()
        data = response.json()
    redis_client.setex(key, settings.context_cache_ttl, json.dumps(data))
    return data
