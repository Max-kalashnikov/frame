from datetime import datetime

request_id = input("Номер заявки: ").strip()
status = input("Статус (new/in_progress/closed): ").strip().lower()
priority = input("Приоритет (high/normal): ").strip().lower()
hours_since_creation = float(input("Часов с момента создания: ").strip())

response_limit_hours = 4.0
created_at = datetime.now()
is_high_priority = priority == "high"
is_overdue = hours_since_creation >= response_limit_hours

print(f"\nЗаявка №{request_id}")
print(f"Статус: {status}")
print(f"Время создания: {created_at:%d.%m.%Y %H:%M}")

if status == "closed":
    print("Заявка закрыта. Дополнительные действия не требуются.")
elif is_high_priority or is_overdue:
    print("Срочно: заявка требует реакции оператора.")
else:
    remaining_hours = response_limit_hours - hours_since_creation
    print(f"Заявка в работе. До контрольного срока: {remaining_hours:.1f} ч.")
