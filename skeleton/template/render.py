import re

from typing import Mapping

TEMPLATE_VARIABLE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")

def render(
    content: str,
    variables: Mapping[str, str],
) -> str:

    def replace(match: re.Match) -> str:

        name = match.group(1)

        if name not in variables:
            raise ValueError(f"Unknown template variable: {name!r}")

        return variables[name]

    return TEMPLATE_VARIABLE.sub(replace, content)