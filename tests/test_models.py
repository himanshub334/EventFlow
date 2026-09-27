from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from app.models import AdEvent

def test_valid_event():
    e=AdEvent(event_id="evt-1",event_type="impression",campaign_id="c1",device_id="d1",timestamp=datetime.now(timezone.utc))
    assert e.event_type=="impression"

def test_invalid_event_type():
    with pytest.raises(ValidationError):
        AdEvent(event_id="evt-1",event_type="unknown",campaign_id="c1",device_id="d1",timestamp=datetime.now(timezone.utc))
