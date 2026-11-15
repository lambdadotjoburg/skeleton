from ..cmd.command import Command, Values

def custom_help_parser(
    definition: Command.Definition,
    tokens: list[str],
) -> Values:

    return {
        "commands": [
            token.removeprefix("--")
            for token in tokens
        ],
    }