
import json
import os
import shutil
import subprocess

from pathlib import Path

FRONTEND_SCRIPTS = {
    "--serve": "serve",
    "--build": "build",
    "--preview": "preview",
    "--clean": "clean",
    "--purge": "purge",
}

def run_frontend_script(
    command: str,
    project_root: Path,
) -> int:

    if command not in FRONTEND_SCRIPTS:
        print(f"Error: Unsupported frontend command: {command}")
        return 2

    project_root = project_root.resolve()

    # Read the client's generated configuration.
    # Do not read the framework's templates directory here.

    layout_path = project_root / "skeleton-layout.json"

    if not layout_path.is_file():
        print(
            "Error: Skeleton project layout not found: "
            f"{layout_path}"
        )
        return 1

    try:
        with layout_path.open("r", encoding="utf-8") as file:
            layout = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Error reading Skeleton project layout: {error}")
        return 1

    if not isinstance(layout, dict):
        print(
            "Error: Skeleton project layout must contain "
            "a JSON object."
        )
        return 1

    frontend_config = layout.get("frontend")

    if not isinstance(frontend_config, dict):
        print(
            "Error: 'frontend' must be an object in "
            "skeleton-layout.json."
        )
        return 1

    frontend_name = frontend_config.get("directory")

    if (
        not isinstance(frontend_name, str)
        or not frontend_name.strip()
        or Path(frontend_name).is_absolute()
        or len(Path(frontend_name).parts) != 1
        or frontend_name in (".", "..")
    ):
        print(
            "Error: 'frontend.directory' must be a single "
            "relative directory name in skeleton-layout.json."
        )
        return 1

    frontend_root = project_root / frontend_name
    package_json = frontend_root / "package.json"

    if not package_json.is_file():
        print(
            "Error: Frontend package manifest not found: "
            f"{package_json}"
        )
        return 1

    try:
        with package_json.open("r", encoding="utf-8") as file:
            package = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Error reading frontend package.json: {error}")
        return 1

    if not isinstance(package, dict):
        print(
            "Error: Frontend package manifest must contain "
            f"a JSON object: {package_json}"
        )
        return 1

    script_name = FRONTEND_SCRIPTS[command]
    scripts = package.get("scripts", {})

    if not isinstance(scripts, dict) or script_name not in scripts:
        print(
            f"Error: Frontend script {script_name!r} "
            f"is not defined in {package_json}."
        )
        return 1

    npm = shutil.which("npm")

    if npm is None:
        print("Error: npm was not found. Install Node.js and npm.")
        return 1

    print(
        f"INFO: Running frontend script '{script_name}' "
        f"in {frontend_root}"
    )

    try:
        if os.name == "nt":
            # npm is commonly exposed as npm.cmd on Windows.
            command_line = subprocess.list2cmdline(
                [npm, "run", script_name]
            )

            result = subprocess.run(
                command_line,
                cwd=frontend_root,
                shell=True,
                check=False,
            )

        else:
            result = subprocess.run(
                [npm, "run", script_name],
                cwd=frontend_root,
                check=False,
            )

        return result.returncode

    except OSError as error:
        print(f"Error running frontend script: {error}")
        return 1


def main(
    argv: list[str],
    framework_root: Path,
    project_root: Path,
) -> int:

    args = argv

    framework_root = framework_root.resolve()
    project_root = project_root.resolve()

    if not args:
        print(
            "Usage: skeleton "
            "--config | --init | --install | --start | "
            "--serve | --build | --preview | --clean | "
            "--purge | --quickstart | --quick-start"
        )
        return 0

    command = args[0]

    if command == "--config":

        from skeleton.infrastructure.bootstrap.src.config import config

        config(
            framework_root=framework_root,
            project_root=project_root,
        )

        return 0

    if command == "--init":

        from skeleton.infrastructure.bootstrap.src.commands.client.init import (
            init,
        )

        init(
            framework_root=framework_root,
            project_root=project_root,
        )

        return 0

    if command == "--install":

        from skeleton.infrastructure.bootstrap.src.commands.client.install import (
            install,
        )

        install(
            framework_root=framework_root,
            project_root=project_root,
        )

        return 0

    if command == "--start":

        from skeleton.infrastructure.runners.src.main import run

        run(
            framework_root=framework_root,
            project_root=project_root,
            argv=args,
        )

        return 0

    if command in FRONTEND_SCRIPTS:

        return run_frontend_script(
            command=command,
            project_root=project_root,
        )

    if command in ("--quickstart", "--quick-start"):

        from skeleton.infrastructure.bootstrap.src.config import config

        from skeleton.infrastructure.bootstrap.src.commands.client.init import (
            init,
        )

        from skeleton.infrastructure.bootstrap.src.commands.client.install import (
            install,
        )

        print("\n[1/3] Generating project configuration...\n")

        config(
            framework_root=framework_root,
            project_root=project_root,
        )

        print("\n[2/3] Initializing project...\n")

        init(
            framework_root=framework_root,
            project_root=project_root,
        )

        print("\n[3/3] Installing project dependencies...\n")

        install(
            framework_root=framework_root,
            project_root=project_root,
        )

        print("\nQuickstart completed successfully.")
        print("Run 'skeleton --start' to start your project.")

        return 0

    raise ValueError(f"Unknown client command: {command}")
