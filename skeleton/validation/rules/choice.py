from typing import Any
from collections.abc import Iterable

def choice(options: Iterable[str]):

    allowed = frozenset(options)

    def validate(value: Any) -> str | None:

        if value not in allowed:
            return (
                "Invalid value. "
                f"Choose one of: {', '.join(sorted(allowed))}"
            )

        return None

    return validate