"""JSON storage helpers for the request monitoring application."""

import json
from pathlib import Path
from typing import Any

JsonRecords = list[dict[str, Any]]


def load_data(file_path: Path) -> JsonRecords:
    """Load a list of records from JSON or return an empty list on errors."""
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []
    return [record for record in data if isinstance(record, dict)]


def save_data(file_path: Path, data: JsonRecords) -> None:
    """Save records to JSON using a context manager."""
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as error:
        raise RuntimeError(
            f"Не удалось сохранить файл {file_path.name}.") from error
