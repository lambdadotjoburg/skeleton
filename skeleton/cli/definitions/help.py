from typing import Any

from ...context.roles import Role

from ...context.context import CLIContext
from ...decorators.command import command

from ...parsers.help import custom_help_parser
from ..implementations.help import help as execute_help

@command(
    
    name="help",

    roles=[Role.CLIENT, Role.FRAMEWORK],

    parser=custom_help_parser,

    arguments={
        "commands": ["*"]
    },

    defaults={
        "commands": []
    },
    
    description="Show help for skeleton commands!",
)
def help(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_help(
        values=values,
        context=context,
    )