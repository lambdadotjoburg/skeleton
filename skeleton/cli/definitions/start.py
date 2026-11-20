from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

# runtime server/orcherstration mode
from ...runtime.mode import RuntimeMode

from ..implementations.start import start as execute_start

@command(
    
    name="start",

    roles=[Role.CLIENT],

    description=(
        "start skeleton orchestration "
        "engine & launch gateway server!"
    ),

    arguments={

        "mode": [
            mode.value
            for mode in RuntimeMode
        ],
        
        # maybe allow client to
        # explicitly override gateway
        # port + host

        # "port": ["8000"],
        # "host": ["127.0.0.1"],
    },

    defaults={
        
        "mode": None,

        # maybe allow client to
        # explicitly override gateway
        # port + host

        # "port": "8000",
        # "host": "127.0.0.1",
    },
)
def start(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_start(
        values=values,
        context=context,
    )