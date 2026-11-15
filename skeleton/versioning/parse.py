import re

VERSION_PATTERN = re.compile(
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
)

def parse_version(version: str) -> tuple[int, int, int] | None:

    match = VERSION_PATTERN.fullmatch(version)

    if match is None:
        return None

    return (
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
    )