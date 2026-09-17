"""Safe console input helpers."""


def input_text(prompt: str) -> str:
    """Request non-empty text from the user."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Введите непустое значение.")


def input_int(prompt: str, minimum: int = 1) -> int:
    """Request an integer not lower than the provided minimum."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Введите целое число.")
            continue
        if value < minimum:
            print(f"Введите число не меньше {minimum}.")
            continue
        return value


def input_choice(prompt: str, choices: set[str]) -> str:
    """Request one value from a set of allowed choices."""
    while True:
        value = input(prompt).strip().lower()
        if value in choices:
            return value
        print(f"Допустимые значения: {', '.join(sorted(choices))}.")
