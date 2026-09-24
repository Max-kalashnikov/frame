"""Classes and collection helpers for user requests."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from users import User, get_or_create_user

PRIORITIES = {"высокий", "обычный"}
STATUSES = {"новая", "в работе", "закрыта", "отменена"}


class Request:
    """A user request registered in the monitoring system."""

    def __init__(
        self,
        request_id: int,
        title: str,
        user: User,
        priority: str,
        status: str = "новая",
        created_at: str | None = None,
        response_limit_hours: int = 4,
    ) -> None:
        self.id = request_id
        self.title = title.strip()
        self.user = user
        self.priority = priority.strip().lower()
        self.status = status.strip().lower()
        self.created_at = created_at or datetime.now().isoformat(
            timespec="minutes"
        )
        self.response_limit_hours = response_limit_hours
        self._validate()

    def _validate(self) -> None:
        """Validate the state needed to create a request object."""
        if not self.title:
            raise ValueError(
                "Название заявки не может быть пустым.")
        if self.priority not in PRIORITIES:
            raise ValueError("Приоритет должен быть высокий или обычный.")
        if self.status not in STATUSES:
            raise ValueError("Недопустимый статус заявки.")
        if not self.validate_response_limit(self.response_limit_hours):
            raise ValueError("Срок реакции должен быть положительным.")

    @staticmethod
    def validate_response_limit(response_limit_hours: int) -> bool:
        """Return whether a response time limit is a positive integer."""
        return isinstance(response_limit_hours,
                          int) and response_limit_hours > 0

    @classmethod
    def from_data(cls, data: dict[str, Any], users: list[User]) -> "Request":
        """Create a request object from a JSON record."""
        return cls(
            request_id=data["id"],
            title=data["title"],
            user=_find_user(data, users),
            priority=data["priority"],
            status=data.get("status", "новая"),
            created_at=data.get("created_at"),
            response_limit_hours=data.get("response_limit_hours", 4),
        )

    def to_data(self) -> dict[str, Any]:
        """Convert the object to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "user_id": self.user.id,
            "user_name": self.user.name,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at,
            "response_limit_hours": self.response_limit_hours,
        }

    def hours_since_creation(
            self, current_time: datetime | None = None) -> float:
        """Calculate the elapsed time since the request was created."""
        try:
            created_at = datetime.fromisoformat(self.created_at)
        except ValueError:
            return 0.0
        now = current_time or datetime.now()
        return max((now - created_at).total_seconds() / 3600, 0.0)

    def is_closed(self) -> bool:
        """Return whether no further work is needed on the request."""
        return self.status in {"закрыта", "отменена"}

    def needs_attention(self, current_time: datetime | None = None) -> bool:
        """Return whether an open request needs an operator's attention."""
        if self.is_closed():
            return False
        return self.priority == "высокий" or (
            self.hours_since_creation(
                current_time) >= self.response_limit_hours
        )

    def change_status(self, new_status: str) -> bool:
        """Change the status and return whether the object was modified."""
        normalized_status = new_status.strip().lower()
        if normalized_status not in STATUSES:
            raise ValueError("Недопустимый статус заявки.")
        if self.status == normalized_status:
            return False
        self.status = normalized_status
        return True

    def cancel(self) -> bool:
        """Cancel an open request without removing it from the collection."""
        if self.is_closed():
            return False
        self.status = "отменена"
        return True

    def __str__(self) -> str:
        """Return a concise representation of the request."""
        return f"Заявка №{self.id}: {self.title} ({self.status})"

    @property
    def user_name(self) -> str:
        """Return the related user's name for display and JSON."""
        return self.user.name


def create_request(
    requests: list[Request],
    users: list[User],
    title: str,
    user_name: str,
    priority: str,
    response_limit_hours: int = 4,
) -> Request:
    """Create a request object, add it to the collection and return it."""
    request = Request(
        request_id=max((item.id for item in requests), default=0) + 1,
        title=title,
        user=get_or_create_user(users, user_name),
        priority=priority,
        response_limit_hours=response_limit_hours,
    )
    requests.append(request)
    return request


def _find_user(data: dict[str, Any], users: list[User]) -> User:
    """Find a stored user by identifier or restore one from legacy data."""
    user_id = data.get("user_id")
    user = next((item for item in users if item.id == user_id), None)
    if user is not None:
        return user
    return get_or_create_user(users, data["user_name"])


def get_request_by_id(requests: list[Request],
                      request_id: int) -> Request | None:
    """Return a request object by its identifier."""
    return next((item for item in requests if item.id == request_id), None)


def find_requests(requests: list[Request], query: str) -> list[Request]:
    """Find request objects by a substring in title or user name."""
    normalized_query = query.strip().casefold()
    if not normalized_query:
        return []
    return [
        item
        for item in requests
        if normalized_query in item.title.casefold()
        or normalized_query in item.user_name.casefold()
    ]


def filter_requests_by_status(
        requests: list[Request], status: str) -> list[Request]:
    """Return objects that have the requested status."""
    return [item for item in requests if item.status == status]


def sort_requests(requests: list[Request]) -> list[Request]:
    """Sort request objects by priority and then by creation time."""
    priority_order = {"высокий": 0, "обычный": 1}
    return sorted(
        requests,
        key=lambda item: (
            priority_order.get(
                item.priority,
                2),
            item.created_at),
    )
