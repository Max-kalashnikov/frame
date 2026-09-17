"""Functions for creating, searching and sorting user requests."""

from datetime import datetime
from typing import Any

Request = dict[str, Any]
PRIORITIES = {"high", "normal"}


def create_request(
    requests: list[Request],
    title: str,
    user_name: str,
    priority: str,
    response_limit_hours: int = 4,
) -> Request:
    """Create a request, add it to the list and return the new record."""
    normalized_title = title.strip()
    normalized_user_name = user_name.strip()
    normalized_priority = priority.strip().lower()
    if not normalized_title or not normalized_user_name:
        raise ValueError("Название и имя пользователя не могут быть пустыми.")
    if normalized_priority not in PRIORITIES:
        raise ValueError("Приоритет должен быть high или normal.")
    if response_limit_hours <= 0:
        raise ValueError("Срок реакции должен быть положительным.")

    next_id = max((request["id"] for request in requests), default=0) + 1
    request = {
        "id": next_id,
        "title": normalized_title,
        "user_name": normalized_user_name,
        "priority": normalized_priority,
        "status": "new",
        "created_at": datetime.now().isoformat(timespec="minutes"),
        "response_limit_hours": response_limit_hours,
    }
    requests.append(request)
    return request


def get_request_by_id(
    requests: list[Request], request_id: int
) -> Request | None:
    """Return a request by its identifier."""
    for request in requests:
        if request["id"] == request_id:
            return request
    return None


def find_requests(requests: list[Request], query: str) -> list[Request]:
    """Find requests by a substring in title or user name."""
    normalized_query = query.strip().casefold()
    if not normalized_query:
        return []
    return [
        request
        for request in requests
        if normalized_query in request["title"].casefold()
        or normalized_query in request["user_name"].casefold()
    ]


def filter_requests_by_status(
    requests: list[Request], status: str
) -> list[Request]:
    """Return requests that have the requested status."""
    return [request for request in requests if request["status"] == status]


def sort_requests(requests: list[Request]) -> list[Request]:
    """Sort requests by priority and then by creation time."""
    priority_order = {"high": 0, "normal": 1}
    return sorted(
        requests,
        key=lambda request: (
            priority_order.get(request["priority"], 2),
            request["created_at"],
        ),
    )
