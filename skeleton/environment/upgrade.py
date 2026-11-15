from pathlib import Path

from .runner import run

def upgrade(
    *,
    python: Path,
    cwd: Path,
    check: bool = False,
    verbose: bool = False,
    description: str = "Upgrading pip ...",
) -> int:
    return run(
        command=[
            str(python),
            "-m",
            "pip",
            "install",
            "--upgrade",
            "pip",
        ],
        cwd=cwd,
        verbose=verbose,
        check=check,
        description=description,
    )