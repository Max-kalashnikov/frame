"""Console interface for the object-oriented request monitoring system."""

from pathlib import Path

from events import RequestEvent, add_event
from monitoring import determine_action, get_statistics
from requests import (
    STATUSES,
    Request,
    create_request,
    find_requests,
    get_request_by_id,
    sort_requests,
)
from storage import (
    load_events,
    load_requests,
    load_users,
    save_events,
    save_requests,
    save_users,
)
from users import User
from utils import input_choice, input_int, input_text 

DATA_DIR = Path("data")
REQUESTS_FILE = DATA_DIR / "requests.json"
EVENTS_FILE = DATA_DIR / "events.json"
USERS_FILE = DATA_DIR / "users.json"


def print_request_information(request: Request) -> None:
    """Print complete information about one request object."""
    print(f"\nЗаявка №{request.id}: {request.title}")
    print(f"Пользователь: {request.user_name}")
    print(f"Статус: {request.status}; приоритет: {request.priority}")
    print(f"Создана: {request.created_at}")


def show_requests(requests: list[Request]) -> None:
    """Print a sorted list of request objects."""
    if not requests:
        print("Список заявок пуст.")
        return
    print("\nID | Статус       | Приоритет | Заявка")
    print("---+--------------+-----------+----------------------------")
    for request in sort_requests(requests):
        print(
            f"{request.id:>2} | {request.status:<12} | "
            f"{request.priority:<9} | {request.title}"
        )


def show_request(request: Request) -> None:
    """Print a request and the action determined by its methods."""
    print_request_information(request)
    print(determine_action(request))


def add_request_from_console(
    requests: list[Request], users: list[User], events: list[RequestEvent]
) -> None:
    """Create a request object from input and record its first event."""
    title = input_text("Тема заявки: ")
    user_name = input_text("Имя пользователя: ")
    priority = input_choice(
        "Приоритет (высокий/обычный): ", {"высокий", "обычный"})
    limit = input_int("Срок реакции в часах: ")
    request = create_request(
        requests,
        users,
        title,
        user_name,
        priority,
        limit)
    add_event(events, request, "created", "Заявка зарегистрирована")
    print(f"Заявка №{request.id} создана.")


def change_status_from_console(
    requests: list[Request], events: list[RequestEvent]
) -> None:
    """Change the status of a found request object and record an event."""
    request = get_request_by_id(requests, input_int("ID заявки: "))
    if request is None:
        print("Заявка не найдена.")
        return
    status = input_choice("Новый статус: ", STATUSES)
    if not request.change_status(status):
        print("У заявки уже установлен этот статус.")
        return
    add_event(events, request, "status_changed", f"Статус изменён на {status}")
    print("Статус обновлён.")


def cancel_request_from_console(
    requests: list[Request], events: list[RequestEvent]
) -> None:
    """Cancel a found request object and record an event."""
    request = get_request_by_id(requests, input_int("ID заявки: "))
    if request is None:
        print("Заявка не найдена.")
        return
    if not request.cancel():
        print("Эту заявку нельзя отменить.")
        return
    add_event(events, request, "отменена", "Заявка отменена")
    print("Заявка отменена.")


def show_urgent_requests(requests: list[Request]) -> None:
    """Print all request objects that require attention."""
    print("\nСрочные заявки:")
    show_requests(
        [request for request in requests if request.needs_attention()])


def show_statistics(requests: list[Request]) -> None:
    """Print aggregated statistics for request objects."""
    statistics = get_statistics(requests)
    print(
        f"\nВсего: {statistics['total']}; новые: {statistics['новая']}; "
        f"в работе: {
            statistics['в работе']}; закрытые: {
            statistics['закрыта']}; "
        f"отменённые: {
            statistics['отменена']}; срочные: {
            statistics['urgent']}."
    )


def save_project_data(
    requests: list[Request], users: list[User], events: list[RequestEvent]
) -> None:
    """Save both collections after a state-changing console operation."""
    save_requests(REQUESTS_FILE, requests)
    save_users(USERS_FILE, users)
    save_events(EVENTS_FILE, events)


def main() -> None:
    """Run the menu using collections of domain objects."""
    users = load_users(USERS_FILE)
    requests = load_requests(REQUESTS_FILE, users)
    events = load_events(EVENTS_FILE, requests)
    while True:
        print(
            "\n=== Система мониторинга пользовательских заявок ===\n"
            "1. Показать заявки\n2. Найти заявку\n3. Создать заявку\n"
            "4. Изменить статус\n5. Отменить заявку\n"
            "6. Показать срочные заявки\n7. Показать статистику\n0. Выход"
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
            add_request_from_console(requests, users, events)
            save_project_data(requests, users, events)
        elif choice == "4":
            change_status_from_console(requests, events)
            save_project_data(requests, users, events)
        elif choice == "5":
            cancel_request_from_console(requests, events)
            save_project_data(requests, users, events)
        elif choice == "6":
            show_urgent_requests(requests)
        else:
            show_statistics(requests)


if __name__ == "__main__":
    main()
