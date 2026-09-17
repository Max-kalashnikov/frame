from datetime import datetime

from monitoring import cancel_request, needs_attention


def make_request(priority: str = "normal", status: str = "new") -> dict:
    return {
        "id": 1,
        "priority": priority,
        "status": status,
        "created_at": "2026-09-17T09:00",
        "response_limit_hours": 4,
    }


def test_high_priority_request_needs_attention() -> None:
    request = make_request(priority="high")
    assert needs_attention(request, datetime(2026, 9, 17, 9, 1))


def test_cancelled_request_does_not_need_attention() -> None:
    request = make_request(priority="high")
    assert cancel_request(request)
    assert not needs_attention(request, datetime(2026, 9, 17, 14, 0))
