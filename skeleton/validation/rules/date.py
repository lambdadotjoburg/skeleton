from typing import Any

from datetime import date

def iso_date(value: Any) -> str | None:

    if not isinstance(value, str):
        return "Expected a date string."

    try:
        date.fromisoformat(value)
    except ValueError:
        return "Expected a valid YYYY-MM-DD date."

    if len(value) != 10:
        return "Expected a valid YYYY-MM-DD date."

    return None