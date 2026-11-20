from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ..implementations.demo import demo as execute_demo

@command(
    
    name="demo",

    roles=[Role.FRAMEWORK],

    description=(
        "Install client project from local dist!"
    ),

    flags=[
        "dry",
        "verbose",
    ],

    arguments={
        "target": "*"
    },

    defaults={
        "target": "./demo"
    },
)
def demo(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_demo(
        values=values,
        context=context
    )