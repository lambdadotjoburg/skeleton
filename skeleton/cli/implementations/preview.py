from typing import Any

from ...decorators.roles import roles
from ...context.roles import Role
from ...context.context import CLIContext

@roles(Role.CLIENT)
def preview(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    client = context.CLIENT

    if client is None:
        raise RuntimeError("Client layout is unavailable.")

    try:

        client.config.require(
            ["skeleton-project.json"]
        )

        outdir = client.frontend.outdir

    except FileNotFoundError as error:

        print(
            "\nCannot preview client application.\n"
            f"{error}"
        )

        return 1

    if not outdir.is_dir():

        print(
            "\n"
            "Cannot preview client application!"
            "\n"
            f"Frontend distribution not found: {outdir}"
            "\n\n"
            "Run skeleton: --dist (--frontend)!"
        )

        return 1

    from .start import start
    from ...runtime.mode import RuntimeMode

    return start(
        values={
            **values,
            "mode": RuntimeMode.PREVIEW.value,
        },
        context=context,
    )