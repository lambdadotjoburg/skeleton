from ..cmd.types import Values
from ..cmd.command import Command

def custom_bump_parser(
    definition: Command.Definition,
    tokens: list[str],
) -> Values:

    from ..cmd.parser import defaults

    values = defaults(definition)

    seen: set[str] = set()
    index = 0

    optional_values = {
        "major",
        "minor",
        "patch",
    }

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
            raise ValueError(
                f"Unknown argument or flag: {token}"
            )

        if name in optional_values:

            if (
                index + 1 < len(tokens)
                and not tokens[index + 1].startswith("--")
            ):
                values[name] = tokens[index + 1]
                index += 2

            else:
                values[name] = True
                index += 1

            continue

        raise ValueError(
            f"Unsupported argument: {token}"
        )

    return values