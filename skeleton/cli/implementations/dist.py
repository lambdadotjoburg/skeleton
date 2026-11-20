import sys

from typing import Any

from ...utils.display import display
from ...context.context import CLIContext

def dist(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    from ...context.mode import Mode
    from ...environment.runner import run

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True

    backend = values.get("backend", False) is True
    frontend = values.get("frontend", False) is True

    if context.mode == Mode.FRAMEWORK:

        framework = context.FRAMEWORK

        command = [
            sys.executable,
            "-m",
            "build",
            "--outdir",
            str(framework.outdir),
        ]

        if dry:
            display(
                description="Framework distribution",
                command=command,
                cwd=framework.root,
                outdir=framework.outdir,
            )

        else:
            return run(
                command,
                cwd=context.root,
                verbose=verbose,
                check=False,
                description="Building Skeleton distribution ...",
            )

        return 0

    if not backend and not frontend:
        backend = True
        frontend = True
    
    client = context.CLIENT

    if client is None:
        raise RuntimeError("Client layout is unavailable.")

    # ------------------------------------------------
    # Backend distribution
    # ------------------------------------------------

    if backend:

        root = client.backend.root

        if not root.is_dir():
            print("Client backend directory not found.")
            return 1

        command = [
            sys.executable,
            "-m",
            "build",
            "--outdir",
            str(client.backend.outdir),
        ]

        if dry:
            display(
                description="Backend distribution",
                command=command,
                cwd=root,
                outdir=client.backend.outdir,
            )

        else:
            result = run(
                command,
                cwd=root,
                verbose=verbose,
                check=False,
                description="Building Client Backend distribution ...",
            )

            if result != 0:
                return result

    # ------------------------------------------------
    # Frontend distribution
    # ------------------------------------------------

    if frontend:

        root = client.frontend.root
        webpack = client.frontend.webpack

        if not root.is_dir():
            print("Client frontend directory not found.")
            return 1

        if not webpack.is_file():
            print(f"Webpack config not found: {webpack}")
            return 1

        command = [
            client.frontend.npm,
            "exec",
            "--",
            "webpack",
            "--config", str(webpack),
            "--env", f"root={client.root}",
            "--env", "mode=production",
        ]

        for key, value in client.runtime.webpack.items():
            command.extend(["--env", f"{key}={value}"])

        if dry:
            display(
                description="Frontend distribution",
                command=command,
                cwd=root,
                outdir=client.frontend.outdir,
            )

        else:
            result = run(
                command,
                cwd=root,
                verbose=verbose,
                check=False,
                description="Building Client Frontend distribution ...",
            )

            if result != 0:
                return result

    if dry:
        print("\nDRY RUN: No distribution artifacts generated!")
    else:
        print("\nDistribution built successfully!")

    return 0
