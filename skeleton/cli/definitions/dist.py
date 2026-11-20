from typing import Any

from ...context.roles import Role

from ...context.context import CLIContext

from ...decorators.command import command

from ..implementations.dist import dist as execute_dist

@command(
    
    name="dist",

    roles=[Role.CLIENT, Role.FRAMEWORK],

    description="Build dist output!",
    
    flags=[
        "dry",
        "verbose",
        "backend",
        "frontend"
    ],
)
def dist(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_dist(
        values=values,
        context=context
    )