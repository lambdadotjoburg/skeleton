import re

from typing import Any

PACKAGE_NAME_PATTERN = re.compile(
    r"[a-z0-9]+(?:-[a-z0-9]+)*"
)

def package_name(value: Any) -> str | None:

    if not isinstance(value, str):
        return "Expected a project name string."

    normalized = re.sub(
        r"[^a-z0-9]+",
        "-",
        value.strip().lower(),
    ).strip("-")

    if not normalized:
        return "Project name cannot produce a valid package name."

    if len(normalized) > 214:
        return "Normalized package name cannot exceed 214 characters."

    if not PACKAGE_NAME_PATTERN.fullmatch(normalized):
        return "Project name cannot produce a valid package name."

    return None