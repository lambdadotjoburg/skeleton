import re

from typing import Any

URL_PREFIX_PATTERN = re.compile(
    r"[a-z0-9]+(?:[-._~][a-z0-9]+)*(?:/[a-z0-9]+(?:[-._~][a-z0-9]+)*)*"
)

def url_prefix(value: Any) -> str | None:

    # The required rule handles missing or non-string values.
    if not isinstance(value, str) or not value.strip():
        return None

    if value != value.lower():
        return "URL prefix must use lowercase characters."

    if URL_PREFIX_PATTERN.fullmatch(value) is None:
        return (
            "Invalid URL prefix"
            "\n"
            "Use only:"
            "\n"
            "lowercase letters, numbers, hyphens, "
            "underscores, dots, or tildes, "
            "separated into path segments with '/'"
        )

    return None