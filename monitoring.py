"""Monitoring and lifecycle functions for user requests."""

from datetime import datetime
from typing import Any

Request = dict[str, Any]
Event = dict[str, Any]
STATUSES = {"new", "in_progress", "closed", "cancelled"}


def hours_since_creation(
    request: Request, current_time: datetime | None = None
) -> float:
    """Calculate how many hours have passed since a request was created."""
    try:
        created_at = datetime.fromisoformat(request["created_at"])
    except (KeyError, TypeError, ValueError):
        return 0.0
    now = current_time or datetime.now()
    return max((now - created_at).total_seconds() / 3600, 0.0)


def determine_action(
    status: str, is_high_priority: bool, is_overdue: bool
) -> str:
    """Return the action message from the initial PR1 scenario."""
    if status in {"closed", "cancelled"}:
        return "Заявка завершена. Дополнительные действия не требуются."
    if is_high_priority or is_overdue:
        return "Срочно: заявка требует реакции оператора."
    return "Заявка в работе. Срочная реакция не требуется."


def needs_attention(
    request: Request, current_time: datetime | None = None
) -> bool:
    """Check whether an open request requires urgent attention."""
    if request["status"] in {"closed", "cancelled"}:
        return False
    is_high_priority = request["priority"] == "high"
    is_overdue = hours_since_creation(request, current_time) >= request[
        "response_limit_hours"
    ]
    return is_high_priority or is_overdue


def change_request_status(request: Request, new_status: str) -> bool:
    """Change a request status and return whether it was changed."""
    if new_status not in STATUSES:
        raise ValueError("Недопустимый статус заявки.")
    if request["status"] == new_status:
        return False
    request["status"] = new_status
    return True


def cancel_request(request: Request) -> bool:
    """Cancel an open request."""
    if request["status"] in {"closed", "cancelled"}:
        return False
    request["status"] = "cancelled"
    return True


def add_event(
    events: list[Event], request_id: int, event_type: str, comment: str
) -> Event:
    """Add an event to the request history."""
    event = {
        "id": max((item["id"] for item in events), default=0) + 1,
        "request_id": request_id,
        "event_type": event_type,
        "comment": comment.strip(),
        "created_at": datetime.now().isoformat(timespec="minutes"),
    }
    events.append(event)
    return event


def get_statistics(requests: list[Request]) -> dict[str, int]:
    """Build request statistics using a loop over the collection."""
    statistics = {
        "total": len(requests),
        "new": 0,
        "in_progress": 0,
        "closed": 0,
        "cancelled": 0,
        "urgent": 0,
    }
    for request in requests:
        status = request["status"]
        if status in statistics:
            statistics[status] += 1
        if needs_attention(request):
            statistics["urgent"] += 1
    return statistics
