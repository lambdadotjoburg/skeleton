from skeleton.cmd.types import Values
from skeleton.cmd.command import Command
from skeleton.context.context import CLIContext
from skeleton.decorators.command import command

def custom_client_parser(
    definition: Command.Definition,
    tokens: list[str],
) -> Values:

    assert definition.name == "custom-factory-command"

    return {
        "args": [
            token.removeprefix("--")
            for token in tokens
        ],
    }

@command(
    parser=custom_client_parser,
    factory=lambda context: Command.Definition(
        name="custom-factory-command",
        description=(
            "Custom command for "
            f"{context.root.name}!"
        ),
        arguments={
            "args": ["*"], # any, multiple
        },
    ),
)
def advanced_client_command(
    *,
    values: Values,
    context: CLIContext,
) -> int:

    print(context.root)
    print(values["args"])

    return 0