"""Console interface for the user request monitoring system."""

from pathlib import Path
from typing import Any

from monitoring import (
    STATUSES,
    add_event,
    cancel_request,
    change_request_status,
    determine_action,
    get_statistics,
    hours_since_creation,
    needs_attention,
)
from requests import (
    create_request,
    find_requests,
    get_request_by_id,
    sort_requests,
)
from storage import load_data, save_data
from utils import input_choice, input_int, input_text

DATA_DIR = Path("data")
REQUESTS_FILE = DATA_DIR / "requests.json"
EVENTS_FILE = DATA_DIR / "events.json"
Request = dict[str, Any]


def print_request_information(request: Request) -> None:
    """Print basic information about one request."""
    print(f"\nЗаявка №{request['id']}: {request['title']}")
    print(f"Пользователь: {request['user_name']}")
    print(f"Статус: {request['status']}; приоритет: {request['priority']}")
    print(f"Создана: {request['created_at']}")


def print_action(action: str) -> None:
    """Print an action message for the operator."""
    print(action)


def show_requests(requests: list[Request]) -> None:
    """Print a sorted list of requests."""
    if not requests:
        print("Список заявок пуст.")
        return
    print("\nID | Статус       | Приоритет | Заявка")
    print("---+--------------+-----------+----------------------------")
    for request in sort_requests(requests):
        print(
            f"{request['id']:>2} | {request['status']:<12} | "
            f"{request['priority']:<9} | {request['title']}"
        )


def show_request(request: Request) -> None:
    """Print details and the PR1 action result for one request."""
    print_request_information(request)
    is_high_priority = request["priority"] == "high"
    is_overdue = hours_since_creation(
        request) >= request["response_limit_hours"]
    print_action(determine_action(
        request["status"], is_high_priority, is_overdue))


def add_request_from_console(
    requests: list[Request], events: list[dict[str, Any]]
) -> None:
    """Create a request from user input and save its first event in memory."""
    title = input_text("Тема заявки: ")
    user_name = input_text("Имя пользователя: ")
    priority = input_choice("Приоритет (high/normal): ", {"high", "normal"})
    limit = input_int("Срок реакции в часах: ")
    request = create_request(requests, title, user_name, priority, limit)
    add_event(events, request["id"], "created", "Заявка зарегистрирована")
    print(f"Заявка №{request['id']} создана.")


def change_status_from_console(
    requests: list[Request], events: list[dict[str, Any]]
) -> None:
    """Change request status after a safe lookup by identifier."""
    request_id = input_int("ID заявки: ")
    request = get_request_by_id(requests, request_id)
    if request is None:
        print("Заявка не найдена.")
        return
    status = input_choice("Новый статус: ", STATUSES)
    if not change_request_status(request, status):
        print("У заявки уже установлен этот статус.")
        return
    add_event(events, request_id, "status_changed",
              f"Статус изменён на {status}")
    print("Статус обновлён.")


def cancel_request_from_console(
    requests: list[Request], events: list[dict[str, Any]]
) -> None:
    """Cancel an existing request and record the event."""
    request_id = input_int("ID заявки: ")
    request = get_request_by_id(requests, request_id)
    if request is None:
        print("Заявка не найдена.")
        return
    if not cancel_request(request):
        print("Эту заявку нельзя отменить.")
        return
    add_event(events, request_id, "cancelled", "Заявка отменена")
    print("Заявка отменена.")


def show_urgent_requests(requests: list[Request]) -> None:
    """Print all requests that need attention."""
    urgent_requests = [
        request for request in requests if needs_attention(request)]
    print("\nСрочные заявки:")
    show_requests(urgent_requests)


def show_statistics(requests: list[Request]) -> None:
    """Print aggregated request statistics."""
    statistics = get_statistics(requests)
    message = (
        "\nВсего: {total}; новые: {new}; в работе: {in_progress}; "
        "закрытые: {closed}; отменённые: {cancelled}; "
        "срочные: {urgent}."
    )
    print(message.format(**statistics))


def main() -> None:
    """Run the menu and save changes in JSON files."""
    requests = load_data(REQUESTS_FILE)
    events = load_data(EVENTS_FILE)
    while True:
        print(
            "\n=== Система мониторинга пользовательских заявок ===\n"
            "1. Показать заявки\n"
            "2. Найти заявку\n"
            "3. Создать заявку\n"
            "4. Изменить статус\n"
            "5. Отменить заявку\n"
            "6. Показать срочные заявки\n"
            "7. Показать статистику\n"
            "0. Выход"
        )
        choice = input_choice("Выберите действие: ", set("01234567"))
        if choice == "0":
            print("Работа завершена.")
            return
        if choice == "1":
            show_requests(requests)
        elif choice == "2":
            found_requests = find_requests(requests, input_text("Поиск: "))
            show_requests(found_requests)
            if found_requests:
                show_request(found_requests[0])
        elif choice == "3":
            add_request_from_console(requests, events)
            save_data(REQUESTS_FILE, requests)
            save_data(EVENTS_FILE, events)
        elif choice == "4":
            change_status_from_console(requests, events)
            save_data(REQUESTS_FILE, requests)
            save_data(EVENTS_FILE, events)
        elif choice == "5":
            cancel_request_from_console(requests, events)
            save_data(REQUESTS_FILE, requests)
            save_data(EVENTS_FILE, events)
        elif choice == "6":
            show_urgent_requests(requests)
        else:
            show_statistics(requests)


if __name__ == "__main__":
    main()
