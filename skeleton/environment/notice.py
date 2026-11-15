import os

from ..context.mode import Mode

def advisory() -> str:

    return (
        "\n"
        "Advisory:"
        "\n\n"
        "Skeleton is running outside a virtual environment."
        "\n\n"
        "\t It is recommended to use an isolated environment:"
        "\n\n"
        "\t\t python -m venv .venv"
    )


def activation() -> str:

    if os.name == "nt":

        return (
            "\n"
            "Windows profiles:"
            "\n\n"
            "\t CMD:        .venv\\Scripts\\activate.bat"
            "\n"
            "\t PowerShell: .\\.venv\\Scripts\\Activate.ps1"
            "\n"
            "\t Git Bash:   source ./.venv/Scripts/activate"
        )

    return (
        "\n"
        "Activate the virtual environment:"
        "\n\n"
        "\t source .venv/bin/activate"
    )

def feedback(missing: list[str]) -> str:

    message = (
        "\n" + 
        "Missing skeleton dependencies:" +
        "\n\n" +
        "\n".join(f" - {name}" for name in missing) + 
        "\n\n" + 
        "Install using:" + 
        "\n\n"
    )

    return message + '\t python -m pip install -e ".[dev]"'