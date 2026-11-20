from typing import Any

from ...decorators.roles import roles

from ...context.roles import Role
from ...context.context import CLIContext

@roles(Role.CLIENT)
def script(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    layout = context.CLIENT

    if layout is None:
        raise RuntimeError("Client layout is unavailable.")

    action = values["script"]

    # 1. Resolve package.json
    manifest = layout.frontend.manifest

    # 2. Read and validate the requested script
    scripts = manifest.scripts

    if action not in scripts:
        raise ValueError(
            "\n"
            f"Script {action!r} is not defined!"
            "\n"
            f"{manifest.path}."
        )

    # 3. derive manifest root dir
    cwd=manifest.path.parent

    # 4. Execute using npm run <action>
    from ...environment.runner import run

    command = [
        layout.frontend.npm,
        "run",
        action,
    ]

    return run(
        command,
        cwd=cwd,
        verbose=True,
        check=False,
    )
