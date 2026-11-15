from typing import Any

from ..licenses import LICENSES

def license(value: Any) -> str | None:

    if value not in LICENSES:
        return (
            "Unsupported license. "
            f"Choose one of: {', '.join(LICENSES)}"
        )

    return None