import re

def slug(value: str) -> str:

    value = value.strip().lower()

    value = re.sub(r"[^a-z0-9]+", "-", value)

    return value.strip("-")

def snake(value: str) -> str:

    return slug(value).replace("-", "_")