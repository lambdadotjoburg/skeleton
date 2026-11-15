import keyword

from typing import Any

def identifier(value: Any) -> str | None:

    if not isinstance(value, str):
        return "Expected a Python identifier string."

    if not value.isidentifier():
        return "Expected a valid Python identifier."

    if keyword.iskeyword(value):
        return "Python keywords cannot be used as identifiers."

    return None