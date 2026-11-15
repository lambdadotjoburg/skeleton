import re

from typing import Any

VERSION_PATTERN = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
)

def version(value: Any) -> str | None:

    if not isinstance(value, str):
        return "Expected a version string."

    if not VERSION_PATTERN.fullmatch(value):
        return "Expected MAJOR.MINOR.PATCH."

    return None