from datetime import datetime
from typing import Any, Literal
from pydantic import BaseModel, Field

class AdEvent(BaseModel):
    event_id: str = Field(min_length=1, max_length=128)
    event_type: Literal["impression", "click", "completion"]
    campaign_id: str
    device_id: str
    timestamp: datetime
    country: str = "UNKNOWN"
    metadata: dict[str, Any] = Field(default_factory=dict)
