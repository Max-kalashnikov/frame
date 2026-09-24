"""Class and collection helpers for request history events."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from requests import Request


class RequestEvent:
    """An action in the history of one request."""

    def __init__(
        self,
        event_id: int,
        request: Request,
        event_type: str,
        comment: str,
        created_at: str | None = None,
    ) -> None:
        self.id = event_id
        self.request = request
        self.event_type = event_type.strip()
        self.comment = comment.strip()
        self.created_at = created_at or datetime.now().isoformat(
            timespec="minutes"
        )

    @classmethod
    def from_data(
        cls, data: dict[str, Any], requests: list[Request]
    ) -> "RequestEvent | None":
        """Restore an event and link it to the corresponding request object."""
        request = next(
            (item for item in requests if item.id == data.get("request_id")),
            None,
        )
        if request is None:
            return None
        return cls(
            event_id=data["id"],
            request=request,
            event_type=data["event_type"],
            comment=data["comment"],
            created_at=data.get("created_at"),
        )

    def to_data(self) -> dict[str, Any]:
        """Convert the event to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "request_id": self.request.id,
            "event_type": self.event_type,
            "comment": self.comment,
            "created_at": self.created_at,
        }

    def __str__(self) -> str:
        """Return a concise representation of the history event."""
        return f"{self.created_at}: {self.event_type} - {self.comment}"


def add_event(
    events: list[RequestEvent],
    request: Request,
    event_type: str,
    comment: str,
) -> RequestEvent:
    """Create an event linked to a request and add it to the collection."""
    event = RequestEvent(
        event_id=max((item.id for item in events), default=0) + 1,
        request=request,
        event_type=event_type,
        comment=comment,
    )
    events.append(event)
    return event


def get_events_for_request(
    events: list[RequestEvent], request: Request
) -> list[RequestEvent]:
    """Return event objects belonging to a request object."""
    return [event for event in events if event.request is request]
