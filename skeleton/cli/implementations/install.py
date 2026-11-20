from typing import Any

from ...utils.display import display
from ...decorators.roles import roles
from ...context.roles import Role
from ...context.context import CLIContext

@roles(Role.CLIENT)
def install(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    layout = context.CLIENT

    if layout is None:
        raise RuntimeError("Client layout is unavailable.")

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True
        
    backend = values.get("backend", False) is True
    frontend = values.get("frontend", False) is True

    if not backend and not frontend:
        backend = True
        frontend = True

    try:
        if frontend:
            package = layout.frontend.package

            if not package.is_file():
                raise FileNotFoundError(package)

        if backend:
            pyproject = layout.backend.pyproject

            if not pyproject.is_file():
                raise FileNotFoundError(pyproject)

        layout.config.require("skeleton-project.json")
        layout.config.require("skeleton-dependencies.json")

    except FileNotFoundError as error:
        print(error)
        return 1

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    # Reconcile project manifests!

    from .sync import sync
    
    result = sync(
        values=values,
        context=context
    )

    if result != 0:
        return result

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    from ...environment.runner import run
    
    if backend:

        python = layout.backend.venv_python

        if not python.is_file():
            print(
                "Backend virtual environment is missing or incomplete:\n"
                f"{python}\n"
                "Run skeleton --init first."
            )

        description = "Installing backend dependencies"

        command = [
            str(layout.backend.venv_python),
            "-m",
            "pip",
            "install",
        ]

        if values.get("editable", False) is True:
            command.append("-e")

        command.append(".")

        if dry:
            display(
                description=description,                
                command=command,
                cwd=layout.backend.root,
            )
            
        else:
            result = run(
                command=command,
                cwd=layout.backend.root,
                verbose=verbose,
                check=False,
                description=description,
            )

            if result != 0:
                return result

    if frontend:

        npm = layout.frontend.npm

        description = "Installing frontend dependencies"

        command = [npm, "install"]

        if dry:
            display(
                description=description,
                command=command,
                cwd=layout.frontend.root,
            )

        else:
            result = run(
                command=command,
                cwd=layout.frontend.root,
                verbose=verbose,
                check=False,
                description=description,
            )

            if result != 0:
                return result

    if dry:
        print("\nDRY RUN: No dependencies installed!")

    return 0

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#
    