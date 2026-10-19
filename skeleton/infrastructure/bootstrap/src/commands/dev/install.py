import os, sys
import subprocess

from pathlib import Path

def dev_install(
    framework_root: Path,
) -> None:

    framework_root = framework_root.resolve()

    # ---------------------------------------------------------
    # Install framework root development requirements
    # ---------------------------------------------------------

    requirements = framework_root / "requirements.txt"

    if not requirements.is_file():

        raise FileNotFoundError(
            f"Framework Python requirements not found: "
            f"{requirements}"
        )

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

    print(
        f"INFO: Installing framework Python requirements: "
        f"{requirements}"
    )

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements),
        ],
        cwd=framework_root,
        check=True,
    )

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
    # Create framework gateway environment
    # ---------------------------------------------------------

    gateway_root = (
        framework_root
        / "skeleton"
        / "infrastructure"
        / "gateway"
    )

    venv = gateway_root / ".venv"

    if not venv.is_dir():

        print(f"INFO: Creating framework virtual environment: {venv}")

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

    # ---------------------------------------------------------
    # Install Skeleton and its declared Python dependencies
    # ---------------------------------------------------------

    print(
        f"INFO: Installing Skeleton framework in editable mode: "
        f"{framework_root}"
    )

    subprocess.run(
        [
            str(python),
            "-m",
            "pip",
            "install",
            "-e",
            str(framework_root),
        ],
        cwd=framework_root,
        check=True,
    )

    # ---------------------------------------------------------
    # Install framework Node.js development dependencies
    # ---------------------------------------------------------

    package_json = framework_root / "package.json"

    if not package_json.is_file():

        raise FileNotFoundError(
            f"Framework package manifest not found: {package_json}"
        )

    npm = (
        "npm.cmd"
        if os.name == "nt"
        else "npm"
    )

    print(
        f"INFO: Installing framework Node.js dependencies: "
        f"{framework_root}"
    )

    subprocess.run(
        [npm, "install"],
        cwd=framework_root,
        check=True,
    )

    print("INFO: Framework development installation complete")
