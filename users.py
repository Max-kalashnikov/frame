"""User class and helpers for the request monitoring application."""

from __future__ import annotations

from typing import Any


class User:
    """A user who creates requests in the monitoring system."""

    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name.strip()
        if not self.name:
            raise ValueError("Имя пользователя не может быть пустым.")

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "User":
        """Create a user object from a JSON record."""
        return cls(user_id=data["id"], name=data["name"])

    def to_data(self) -> dict[str, Any]:
        """Convert the user object to a JSON-compatible dictionary."""
        return {"id": self.id, "name": self.name}

    def __str__(self) -> str:
        """Return the user's name as a string representation."""
        return self.name


def get_or_create_user(users: list[User], name: str) -> User:
    """Return an existing user by name or add a new user object."""
    normalized_name = name.strip()
    user = next(
        (item for item in users if item.name.casefold()
         == normalized_name.casefold()),
        None,
    )
    if user is not None:
        return user
    user = User(max((item.id for item in users),
                default=0) + 1, normalized_name)
    users.append(user)
    return user
