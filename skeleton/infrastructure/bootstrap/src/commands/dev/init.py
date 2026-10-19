import os
import sys
import subprocess

from pathlib import Path
def dev_init(
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
    # Generate framework development requirements
    # ---------------------------------------------------------

    requirements = framework_root / "requirements.txt"

    if not requirements.is_file():

        print(
            f"INFO: Creating framework requirements file: "
            f"{requirements}"
        )

        requirements.write_text(
            "build\n"
            "twine\n",
            encoding="utf-8",
        )

    # ---------------------------------------------------------
    # Create framework root virtual environment
    # ---------------------------------------------------------

    venv = framework_root / ".venv"

    if not venv.is_dir():

        print(
            f"INFO: Creating framework virtual environment: "
            f"{venv}"
        )

        subprocess.run(
            [
                sys.executable,
                "-m",
                "venv",
                str(venv),
            ],
            cwd=framework_root,
            check=True,
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

    print("INFO: Framework development initialization complete")