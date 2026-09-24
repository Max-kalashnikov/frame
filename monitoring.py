"""Monitoring functions that operate on request objects."""

from datetime import datetime

from requests import Request, STATUSES


def determine_action(request: Request,
                     current_time: datetime | None = None) -> str:
    """Return an operator action message for a request object."""
    if request.is_closed():
        return "Заявка завершена. Дополнительные действия не требуются."
    if request.needs_attention(current_time):
        return "Срочно: заявка требует реакции оператора."
    return "Заявка в работе. Срочная реакция не требуется."


def get_statistics(requests: list[Request]) -> dict[str, int]:
    """Build statistics for a collection of request objects."""
    statistics = {
        "total": len(requests),
        **{status: 0 for status in STATUSES},
        "urgent": 0,
    }
    for request in requests:
        statistics[request.status] += 1
        if request.needs_attention():
            statistics["urgent"] += 1
    return statistics
