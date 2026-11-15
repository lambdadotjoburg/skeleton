from .types import Values

from .command import Command

def defaults(definition: Command.Definition) -> Values:

    values: Values = {}

    for name, value in definition.defaults.items():

        if isinstance(value, list):
            values[name] = value.copy() # [str | bool]

        else:
            values[name] = value # str or bool

    return values

def parse(
    definition: Command.Definition,
    tokens: list[str],
) -> Values:

    # start with defaults!
    values = defaults(definition)

    seen: set[str] = set()
    index = 0

    while index < len(tokens):

        token = tokens[index]

        if not token.startswith("--") or token == "--":
            raise ValueError(
                f"Expected a named argument or flag, got: {token}"
            )

        name = token.removeprefix("--")

        if name in seen:
            raise ValueError(f"Duplicate argument: {token}")

        seen.add(name)

        if name in definition.flags:

            values[name] = True
            index += 1
            continue

        if name not in definition.arguments:
            raise ValueError(f"Unknown argument or flag: {token}")

        if index + 1 >= len(tokens) or tokens[index + 1].startswith("--"):
            raise ValueError(f"Missing value for argument: {token}")

        allowed = definition.arguments[name]

        # Multiple unrestricted values.
        if allowed == ["*"]:

            index += 1
            collected = []

            while index < len(tokens) and not tokens[index].startswith("--"):
                collected.append(tokens[index])
                index += 1

            values[name] = collected
            continue

        # Single unrestricted value.
        if allowed == "*":

            values[name] = tokens[index + 1]
            index += 2
            continue

        # Single restricted value.
        value = tokens[index + 1]

        if value not in allowed:
            raise ValueError(
                f"Invalid value for {token}: {value!r}."
                f"\nExpected one of: {', '.join(allowed)}"
            )

        values[name] = value
        index += 2

    # Validate required arguments.
    for name in definition.arguments:

        if name not in values:
            raise ValueError(
                f"Missing required argument: --{name}"
            )

    return values