from typing import Any

from ..context.context import CLIContext
from ..context.roles import Role
from ..decorators.roles import roles

@roles(Role.CLIENT)
def quickstart(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    from .config import config
    from .init import init
    from .install import install

    command = context.REGISTRY.get("config")

    if command is None:
        raise NotImplementedError(
            "config is not an identified command!"
        )

    config_values = {
        **command.definition.defaults,
        **values,
    }

    # 1. Generate configuration.

    result = config(
        values=config_values,
        context=context,
    )

    if result != 0:
        return result

    # 2. Initialise the project.

    result = init(
        values=values,
        context=context,
    )

    if result != 0:
        return result

    # 3. Install dependencies.

    result = install(
        values=values,
        context=context,
    )

    return result