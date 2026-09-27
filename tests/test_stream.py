from unittest.mock import patch
from app.stream import publish_event

@patch("app.stream.redis_client")
def test_publish(mock_redis):
    mock_redis.xadd.return_value="1-0"
    assert publish_event({"event_id":"e1"})=="1-0"
    mock_redis.xadd.assert_called_once()
