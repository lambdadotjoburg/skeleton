from typing import Any

def required(value: Any) -> str | None:

    if not isinstance(value, str) or not value.strip():
        return "Value is required."

    return None