from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ..implementations.install import install as execute_install

@command(
    
    name="install",

    roles=[Role.CLIENT],
    
    description="install app dependencies!",

    flags=[

        "dry",
        "verbose",
        "force",
        
        "backend",
        "frontend",

        "editable",
    ],
)
def install(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_install(
        values=values,
        context=context,
    )