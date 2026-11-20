from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ..implementations.init import init as execute_init

@command(
    
    name="init",

    roles=[Role.CLIENT],

    description="initialize & prepare app!",
    
    flags=[

        "dry",
        "verbose",

        "backend",
        "frontend"
        "plugins"
    ],
)
def init(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_init(
        values=values,
        context=context,
    )