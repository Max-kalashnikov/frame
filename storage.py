"""JSON storage helpers for the request monitoring application."""

import json
from pathlib import Path

from events import RequestEvent
from requests import Request
from users import User


def _load_records(file_path: Path) -> list[dict]:
    """Load JSON records or return an empty list when data is unavailable."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, list):
        return []
    return [record for record in data if isinstance(record, dict)]


def load_users(file_path: Path) -> list[User]:
    """Load JSON user records as user objects."""
    users = []
    for data in _load_records(file_path):
        try:
            users.append(User.from_data(data))
        except (KeyError, TypeError, ValueError):
            continue
    return users


def load_requests(file_path: Path, users: list[User]) -> list[Request]:
    """Load JSON request records as request objects."""
    requests = []
    for data in _load_records(file_path):
        try:
            requests.append(Request.from_data(data, users))
        except (KeyError, TypeError, ValueError):
            continue
    return requests


def load_events(file_path: Path,
                requests: list[Request]) -> list[RequestEvent]:
    """Load JSON events and link each one to a request object."""
    events = []
    for data in _load_records(file_path):
        try:
            event = RequestEvent.from_data(data, requests)
        except (KeyError, TypeError, ValueError):
            continue
        if event is not None:
            events.append(event)
    return events


def save_requests(file_path: Path, requests: list[Request]) -> None:
    """Convert request objects to JSON and save them."""
    _save_records(file_path, [request.to_data() for request in requests])


def save_users(file_path: Path, users: list[User]) -> None:
    """Convert user objects to JSON and save them."""
    _save_records(file_path, [user.to_data() for user in users])


def save_events(file_path: Path, events: list[RequestEvent]) -> None:
    """Convert event objects to JSON and save them."""
    _save_records(file_path, [event.to_data() for event in events])


def _save_records(file_path: Path, data: list[dict]) -> None:
    """Save JSON-compatible records and preserve original error handling."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise RuntimeError(
            f"Не удалось сохранить файл {
                file_path.name}.") from error
