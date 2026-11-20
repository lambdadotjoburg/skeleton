from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

# runtime server/orcherstration mode
from ...runtime.mode import RuntimeMode

from ..implementations.preview import preview as execute_preview

@command(
    
    name="preview",

    roles=[Role.CLIENT],
    
    description=(
        "preview frontend build app!"
    ),

    arguments={
        "mode": [RuntimeMode.PREVIEW.value],
    },

    defaults={
        "mode": RuntimeMode.PREVIEW.value,
    },
)
def preview(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_preview(
        values=values,
        context=context,
    )