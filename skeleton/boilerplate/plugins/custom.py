from skeleton.cmd.types import Values
from skeleton.context.context import CLIContext
from skeleton.decorators.command import command

@command(
    name="custom-declarative-command",
    description="Custom declarative command!",
    arguments={
        "args": ["*"], # any, multiple
    },
)
def custom_client_command(
    *,
    values: Values,
    context: CLIContext,
) -> int:

    print(context.root)
    print(values["args"])

    return 0