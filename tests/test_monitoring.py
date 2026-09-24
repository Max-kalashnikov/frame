"""Tests for events, object interaction and JSON persistence."""

from events import RequestEvent, add_event, get_events_for_request
from monitoring import determine_action, get_statistics
from requests import Request
from storage import (
    load_events,
    load_requests,
    load_users,
    save_events,
    save_requests,
    save_users,
)
from users import User


def make_request(priority: str = "обычный", status: str = "новая") -> Request:
    return Request(
        1,
        "Ошибка входа",
        User(1, "Иван"),
        priority,
        status=status,
        created_at="2026-09-17T09:00",
    )


def test_event_keeps_link_to_request_object() -> None:
    request = make_request()
    events: list[RequestEvent] = []
    event = add_event(events, request, "created", "Заявка зарегистрирована")
    assert event.request is request
    assert get_events_for_request(events, request) == [event]
    assert event.to_data()["request_id"] == request.id


def test_cancelled_request_is_not_urgent() -> None:
    request = make_request(priority="высокий")
    assert request.cancel()
    assert "завершена" in determine_action(request)


def test_statistics_uses_object_methods() -> None:
    requests = [make_request("высокий"), make_request("обычный", "закрыта")]
    assert get_statistics(requests)["urgent"] == 1
    assert get_statistics(requests)["закрыта"] == 1


def test_json_storage_restores_object_links(tmp_path) -> None:
    requests_file = tmp_path / "requests.json"
    events_file = tmp_path / "events.json"
    users_file = tmp_path / "users.json"
    request = make_request()
    event = RequestEvent(1, request, "created", "Заявка зарегистрирована")
    save_users(users_file, [request.user])
    save_requests(requests_file, [request])
    save_events(events_file, [event])
    loaded_users = load_users(users_file)
    loaded_requests = load_requests(requests_file, loaded_users)
    loaded_events = load_events(events_file, loaded_requests)
    assert loaded_requests[0].user is loaded_users[0]
    assert loaded_events[0].request is loaded_requests[0]
