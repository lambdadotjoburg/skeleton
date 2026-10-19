import os, sys
import subprocess

from pathlib import Path

from skeleton.infrastructure.bootstrap.src.load import (
    load_layout,
)

def install(
    framework_root: Path,
    project_root: Path,
) -> None:

    framework_root = framework_root.resolve()
    project_root = project_root.resolve()

    # ---------------------------------------------------------
    # Load project configuration
    # ---------------------------------------------------------

    layout = load_layout(
        project_root / "skeleton-layout.json"
    )

    # ---------------------------------------------------------
    # Install backend Python dependencies
    # ---------------------------------------------------------

    backend_root = project_root / layout["backend"]
    requirements = backend_root / "requirements.txt"
    venv = backend_root / ".venv"

    if not requirements.is_file():

        raise FileNotFoundError(
            f"Backend requirements file not found: {requirements}\n"
            "Run 'python run.py --init' from the client directory first."
        )

    if not venv.is_dir():

        print(f"INFO: Creating Python virtual environment: {venv}")

        subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                str(venv),
            ],
            cwd=project_root,
            check=True,
        )

    python = (
        venv / "Scripts" / "python.exe"
        if os.name == "nt"
        else venv / "bin" / "python"
    )

    if not python.is_file():

        raise FileNotFoundError(
            f"Python executable not found in virtual environment: "
            f"{python}"
        )

    print(f"INFO: Installing Python dependencies: {requirements}")

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements),
        ],
        cwd=backend_root,
        check=True,
    )

    # ---------------------------------------------------------
    # Install frontend dependencies
    # ---------------------------------------------------------

    frontend_root = project_root / layout["frontend"]
    package_json = frontend_root / "package.json"

    if not package_json.is_file():

        raise FileNotFoundError(
            f"Frontend package manifest not found: {package_json}\n"
            "Run 'python run.py --init' from the client directory first."
        )

    npm = (
        "npm.cmd"
        if os.name == "nt"
        else "npm"
    )

    print(f"INFO: Installing frontend dependencies: {frontend_root}")

    subprocess.run(
        [npm, "install"],
        cwd=frontend_root,
        check=True,
    )

    print("INFO: Project installation complete")

