import subprocess

from pathlib import Path

from typing import Protocol

class Runner(Protocol):

    def __call__(
        self,
        command: list[str],
        *,
        cwd: Path,
        verbose: bool = False,
        check: bool = False,
        description: str | None = None,
    ) -> int: ...

def run(
    command: list[str],
    *,
    cwd: Path,
    verbose: bool = False,
    check: bool = False,
    description: str | None = None,
) -> int:

    if verbose and description:
        print(f"\n{description}")

    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=check,
            capture_output=not verbose,
            text=True,
        )

    except OSError as error:

        print(f"Failed to execute command: {error}")

        return 1

    if result.returncode != 0:

        if not verbose:

            if result.stdout:
                print(result.stdout, end="")

            if result.stderr:
                print(result.stderr, end="")

        print(
            f"Command failed with exit code "
            f"{result.returncode}."
        )

    return result.returncode