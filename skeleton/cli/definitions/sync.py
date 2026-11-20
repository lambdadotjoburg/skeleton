from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ..implementations.sync import sync as execute_sync

@command(
    
    name="sync",

    roles=[Role.CLIENT],

    description="sync dependencies/manifests!",
    
    flags=[

        "dry",
        "verbose",
        "force",
        
        "backend",
        "frontend",
    ],
)
def sync(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_sync(
        values=values,
        context=context,
    )