from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext

from ...decorators.command import command

from ...parsers.script import custom_script_parser
from ..implementations.script import script as execute_script

@command(
    
    name="script",

    parser=custom_script_parser,

    roles=[Role.CLIENT],

    description=(
        "run a client-defined script "
        "from client's project root!"
    ),
)
def script(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_script(
        values=values,
        context=context,
    )