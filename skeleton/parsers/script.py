from ..cmd.command import Command, Values

def custom_script_parser(
    definition: Command.Definition,
    tokens: list[str],
) -> Values:

    if not tokens:
        raise ValueError(
            "Expected a script name after --script."
        )

    if len(tokens) > 1:
        raise ValueError(
            "Expected exactly one script name after --script."
        )

    return { "script": tokens[0], }