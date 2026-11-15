from typing import Any

from collections.abc import (
    Callable, Mapping, Sequence
)

Rule = Callable[[Any], str | None]

Rules = Mapping[str, Sequence[Rule]]

def validate(
    *,
    values: Mapping[str, Any],
    rules: Rules,
) -> list[str]:

    errors = []

    for name, field_rules in rules.items():

        value = values.get(name)

        for rule in field_rules:

            error = rule(value)

            if error is not None:
                errors.append(f"{name}: {error}")

    return errors