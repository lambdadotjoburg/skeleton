from typing import Any

from ...decorators.roles import roles
from ...context.roles import Role
from ...context.context import CLIContext
from ...layout.client import ClientLayout

def validate(client: ClientLayout) -> bool:

    from ...runtime.mode import RuntimeMode

    if not client.frontend.root.is_dir():
        print("Client frontend directory not found.")
        return False

    if not client.frontend.package.is_file():
        print("Frontend package.json not found.")
        return False

    if not (client.frontend.root / "node_modules").is_dir():
        print("Frontend dependencies not installed. Run --install.")
        return False

    if not client.backend.root.is_dir():
        print("Client backend directory not found.")
        return False

    if not client.backend.venv_python.is_file():
        print("Client backend virtual environment not found. Run --install.")
        return False

    if client.mode == RuntimeMode.DEV:
        if not client.frontend.webpack.is_file():
            print(f"Webpack config not found: {client.frontend.webpack}")
            return False

    elif client.mode == RuntimeMode.PREVIEW:
        if not client.frontend.outdir.is_dir():
            print(f"Frontend distribution not found: {client.frontend.outdir}")
            return False

    return True

@roles(Role.CLIENT)
def start(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    client = context.CLIENT

    if client is None:
        raise RuntimeError("Client layout is unavailable.")

    try:
    
        client.config.require(
            [
                "skeleton-fastapi.json",
                "skeleton-project.json",
                "skeleton-portal.json",
                "skeleton-proxy.json",
                "skeleton-runtime.json",
                "skeleton-schemas.json",
                "skeleton-servers.json",
            ]
        )

        # configured/explicit runtime mode.
        
        mode = values.get("mode")

        if mode is not None:
            
            from ...runtime.mode import RuntimeMode

            client.runtime.mode = RuntimeMode(mode)

        if not validate(client):
            return 1
    
    except FileNotFoundError as error:

        print(
            "\nCannot start skeleton server.\n"
            f"{error}\n\n"
            "Run skeleton --config, --init, --install first!"
        )

        return 1

    framework = context.FRAMEWORK

    engine = framework.engine(client=client)

    from ...engine.run import run

    return run(engine=engine)