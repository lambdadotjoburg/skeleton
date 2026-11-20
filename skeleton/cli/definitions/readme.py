from typing import Any

from ...context.roles import Role

from ...cmd.command import Command

from ...context.context import CLIContext

from ...decorators.command import command

from ..implementations.readme import readme as execute_readme

@command(

    roles=[Role.CLIENT, Role.FRAMEWORK],

    factory=lambda context: Command.Definition(

        name="readme",
        
        arguments={
            "write": "*",
            "section": list(
                context.FRAMEWORK
                .DOCUMENTATION.sections
            ),
        },

        defaults={
            "write": None,
            "section": None,
        },

        description="Inspect/generate Skeleton Framework docs",
    ),
)
def readme(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_readme(
        values=values,
        context=context,
    )