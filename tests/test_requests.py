"""Tests for request and user objects."""

from datetime import datetime

from requests import Request, create_request, find_requests, sort_requests
from users import User


def test_create_request_assigns_identifier_and_links_user() -> None:
    requests: list[Request] = []
    users: list[User] = []
    created = create_request(
        requests, users, "Ошибка входа", "Иван", "высокий"
    )
    assert created.id == 1
    assert created.status == "новая"
    assert created.user is users[0]
    assert created.user.name == "Иван"


def test_same_name_reuses_user_object() -> None:
    requests: list[Request] = []
    users: list[User] = []
    first = create_request(requests, users, "Ошибка входа", "Иван", "обычный")
    second = create_request(
        requests,
        users,
        "Ошибка оплаты",
        "Иван",
        "высокий")
    assert len(users) == 1
    assert first.user is second.user


def test_find_requests_matches_title_case_insensitively() -> None:
    requests: list[Request] = []
    create_request(requests, [], "Ошибка оплаты", "Анна", "обычный")
    assert find_requests(requests, "ОПЛАТЫ") == requests


def test_sort_requests_places_high_priority_first() -> None:
    requests = [
        Request(
            1,
            "Обычная",
            User(1, "Анна"),
            "обычный",
            created_at="2026-09-17T10:00",
        ),
        Request(
            2,
            "Срочная",
            User(2, "Иван"),
            "высокий",
            created_at="2026-09-17T11:00",
        ),
    ]
    assert [request.id for request in sort_requests(requests)] == [2, 1]


def test_request_methods_change_state_and_check_attention() -> None:
    request = Request(
        1,
        "Ошибка входа",
        User(1, "Иван"),
        "обычный",
        created_at="2026-09-17T09:00",
    )
    assert request.needs_attention(datetime(2026, 9, 17, 13, 0))
    assert request.change_status("в работе")
    assert request.cancel()
    assert request.status == "отменена"
    assert not request.needs_attention(datetime(2026, 9, 17, 14, 0))


def test_request_json_conversion_restores_user_object() -> None:
    users: list[User] = []
    request = Request.from_data(
        {
            "id": 3,
            "title": "Ошибка оплаты",
            "user_name": "Анна",
            "priority": "обычный",
            "status": "новая",
            "created_at": "2026-09-17T10:00",
            "response_limit_hours": 8,
        },
        users,
    )
    assert request.to_data()["id"] == 3
    assert request.to_data()["response_limit_hours"] == 8
    assert request.user is users[0]
