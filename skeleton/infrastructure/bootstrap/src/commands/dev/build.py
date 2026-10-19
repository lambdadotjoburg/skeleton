import os, subprocess
from pathlib import Path

def dev_build(
    framework_root: Path,
) -> None:

    framework_root = framework_root.resolve()

    # ---------------------------------------------------------
    # Validate framework package configuration
    # ---------------------------------------------------------

    pyproject = framework_root / "pyproject.toml"

    if not pyproject.is_file():

        raise FileNotFoundError(
            f"Framework Python package configuration not found: "
            f"{pyproject}"
        )

    # ---------------------------------------------------------
    # Validate framework root development environment
    # ---------------------------------------------------------

    venv = framework_root / ".venv"

    if not venv.is_dir():

        raise FileNotFoundError(
            f"Framework virtual environment not found: {venv}. "
            "Run --dev-init first."
        )

    python = (
        venv / "Scripts" / "python.exe"
        if os.name == "nt"
        else venv / "bin" / "python"
    )

    if not python.is_file():

        raise FileNotFoundError(
            f"Framework Python executable not found: {python}"
        )

    # ---------------------------------------------------------
    # Validate Python build requirements
    # ---------------------------------------------------------

    requirements = framework_root / "requirements.txt"

    if not requirements.is_file():

        raise FileNotFoundError(
            f"Framework Python requirements not found: "
            f"{requirements}"
        )

    # ---------------------------------------------------------
    # Build distributable Python package
    # ---------------------------------------------------------

    print(
        f"INFO: Building Skeleton Python package: "
        f"{framework_root}"
    )

    subprocess.run(
        [
            str(python),
            "-m",
            "build",
        ],
        cwd=framework_root,
        check=True,
    )

    print("INFO: Skeleton Python package build complete")