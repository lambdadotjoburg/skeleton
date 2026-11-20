from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ..implementations.purge import purge as execute_purge

@command(
    
    name="purge",

    roles=[Role.CLIENT, Role.FRAMEWORK],

    description="purge build/dist artifacts!",
    
    flags=[
        "dry",
        "verbose",
        "frontend",
        "backend",
    ],
)
def purge(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_purge(
        values=values,
        context=context,
    )