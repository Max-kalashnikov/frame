from requests import create_request, find_requests, sort_requests


def test_create_request_assigns_identifier() -> None:
    requests = []
    created = create_request(requests, "Ошибка входа", "Иван", "high")
    assert created["id"] == 1
    assert requests[0]["status"] == "new"


def test_find_requests_matches_title_case_insensitively() -> None:
    requests = []
    create_request(requests, "Ошибка оплаты", "Анна", "normal")
    assert find_requests(requests, "ОПЛАТЫ") == requests


def test_sort_requests_places_high_priority_first() -> None:
    requests = [
        {"id": 1, "priority": "normal", "created_at": "2026-09-17T10:00"},
        {"id": 2, "priority": "high", "created_at": "2026-09-17T11:00"},
    ]
    assert [request["id"] for request in sort_requests(requests)] == [2, 1]
