from typing import Any

from ...cmd.command import Command

from ...context.roles import Role
from ...context.context import CLIContext

from ...decorators.command import command

from ..implementations.quickstart import quickstart as execute_quickstart

@command(

    roles=[Role.CLIENT],

    factory=lambda context: Command.Definition(

        name="quickstart",
        
        description=(
            "quick start an application, "
            "--config + --init + --install"
        ),

        flags=[
            "dry",
            "verbose",
        ],

        arguments={
            "profile": sorted(
                context.FRAMEWORK
                .BOILERPLATE.profiles
            ),
        },

        defaults={
            "profile": "vanilla",
        },
    ),
)
def quickstart(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_quickstart(
        values=values,
        context=context,
    )