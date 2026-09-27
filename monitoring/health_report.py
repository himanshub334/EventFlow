import json
from datetime import datetime, timezone
from pathlib import Path
import boto3, redis
from pymongo import MongoClient
from app.config import settings
from app.stream import pending_count

def main():
    report={"generated_at":datetime.now(timezone.utc).isoformat(),"checks":{}}
    try:
        r=redis.Redis.from_url(settings.redis_url); r.ping()
        report["checks"]["redis"]="UP"; report["checks"]["stream_pending"]=pending_count()
    except Exception as e: report["checks"]["redis"]=f"DOWN: {e}"
    try:
        MongoClient(settings.mongo_url).admin.command("ping")
        report["checks"]["mongodb"]="UP"
    except Exception as e: report["checks"]["mongodb"]=f"DOWN: {e}"
    try:
        sqs=boto3.client("sqs",region_name=settings.aws_region,endpoint_url=settings.aws_endpoint_url)
        a=sqs.get_queue_attributes(QueueUrl=settings.sqs_queue_url,AttributeNames=["ApproximateNumberOfMessages"])
        report["checks"]["sqs_visible"]=int(a["Attributes"].get("ApproximateNumberOfMessages",0))
    except Exception as e: report["checks"]["sqs"]=f"UNAVAILABLE: {e}"
    Path("health-report.json").write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=="__main__": main()
