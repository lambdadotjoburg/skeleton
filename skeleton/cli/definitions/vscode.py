from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ..implementations.vscode import vscode as execute_vscode

@command(
    
    name="vscode",

    roles=[Role.CLIENT, Role.FRAMEWORK],

    description="Generate .vscode/settings.json config!",

    flags=["dry", "verbose",],

    arguments={
        # eventually, these feature args
        # should be dynamically obtained!
        "feature": ["mypy", "markdown",],
    }
)
def vscode(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_vscode(
        values=values,
        context=context,
    )