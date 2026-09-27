import json
from collections import Counter

def handler(event, context):
    counts = Counter()
    for record in event.get("Records", []):
        body = json.loads(record["body"])
        counts[(body.get("campaign_id"), body.get("event_type"))] += 1
    return {"statusCode":200,"aggregates":[
        {"campaign_id":c,"event_type":t,"count":n}
        for (c,t),n in counts.items()
    ]}
