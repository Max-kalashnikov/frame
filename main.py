from datetime import datetime


def print_request_information(request_id, status, created_at):
    """Выводит основные сведения о заявке."""
    print(f"\nЗаявка №{request_id}")
    print(f"Статус: {status}")
    print(f"Время создания: {created_at:%d.%m.%Y %H:%M}")


def determine_action(status, is_high_priority, is_overdue):
    """Определяет, нужна ли оператору срочная реакция."""
    if status == "closed":
        return "Заявка закрыта. Дополнительные действия не требуются."
    if is_high_priority or is_overdue:
        return "Срочно: заявка требует реакции оператора."
    return "Заявка в работе. Срочная реакция не требуется."


def print_action(action):
    """Выводит решение системы для оператора."""
    print(action)


request_id = input("Номер заявки: ").strip()
status = input("Статус (new/in_progress/closed): ").strip().lower()
priority = input("Приоритет (high/normal): ").strip().lower()
hours_since_creation = float(input("Часов с момента создания: ").strip())

response_limit_hours = 4.0
created_at = datetime.now()
is_high_priority = priority == "high"
is_overdue = hours_since_creation >= response_limit_hours

print_request_information(request_id, status, created_at)
action = determine_action(status, is_high_priority, is_overdue)
print_action(action)