# Система мониторинга пользовательских заявок

Консольное приложение для регистрации и контроля пользовательских заявок. Проект развивается в рамках практических работ по Python: сценарий ПР1 расширен в ПР2 с помощью модулей, коллекций, JSON-файлов, циклов и обработки исключений.

## Возможности

- просмотр заявок, отсортированных по приоритету и времени создания;
- поиск по теме заявки или имени пользователя;
- создание заявок с проверкой введённых данных;
- смена статуса и отмена заявок;
- автоматическое выделение срочных заявок;
- подсчёт статистики по статусам;
- сохранение заявок и событий в JSON.

## Преемственность ПР1

Функция `determine_action()` сохраняет логику начального сценария ПР1: она сообщает оператору, требуется ли срочная реакция. В ПР2 эта проверка применяется к каждой заявке из коллекции.

## Структура проекта

```text
frame/
├── main.py              # консольное меню и вывод данных
├── requests.py          # создание, поиск, фильтрация и сортировка заявок
├── monitoring.py        # статусы, срочность, события и статистика
├── storage.py           # загрузка и сохранение JSON
├── utils.py             # безопасный ввод данных
├── data/
│   ├── requests.json    # заявки
│   └── events.json      # события обработки заявок
├── tests/
│   ├── test_requests.py
│   └── test_monitoring.py
├── requirements.txt
└── .flake8
```

## Основные функции

| Модуль | Функции |
| --- | --- |
| `requests.py` | `create_request`, `find_requests`, `filter_requests_by_status`, `sort_requests` |
| `monitoring.py` | `needs_attention`, `determine_action`, `change_request_status`, `cancel_request`, `add_event`, `get_statistics` |
| `storage.py` | `load_data`, `save_data` |
| `utils.py` | `input_text`, `input_int`, `input_choice` |

Все основные функции содержат docstring и аннотации типов.

## Формат данных

`data/requests.json` хранит список словарей. Каждая заявка содержит `id`, `title`, `user_name`, `priority`, `status`, `created_at` и `response_limit_hours`.

`data/events.json` хранит историю действий: `id`, `request_id`, `event_type`, `comment` и `created_at`.

## Установка

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
python main.py
```

## Проверка

```bash
pytest
flake8
```