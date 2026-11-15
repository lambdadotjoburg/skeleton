from typing import Any
from pathlib import Path

from ..decorators.roles import roles
from ..context.roles import Role
from ..context.context import CLIContext

def get_target(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> Path:

    target = Path(
        values.get("target", "./demo")
    ).expanduser()

    if not target.is_absolute():
        target = context.cwd / target

    return target.resolve()

def get_distribution(
    *,
    outdir: Path,
) -> Path | None:

    if not outdir.is_dir():
        print(
            "\n"
            "Framework distribution not found."
            "\n"
            "Run --dist before creating a demo client."
            "\n"
        )
        return None

    wheels = list(outdir.glob("*.whl"))

    if not wheels:
        print(
            "\n"
            "Framework wheel not found in: \n"
            f"\n{outdir}"
            "\n\n"
            "Run --dist before creating a demo client."
            "\n"
        )
        return None

    if len(wheels) > 1:
        print(
            "\n"
            "Multiple framework wheels found in: \n"
            f"\n{outdir}"
            "\n\n"
            "First clean the distribution directory and run --dist again.\n"
        )
        return None

    return wheels[0]

def prepare_target(
    *,
    target: Path,
) -> bool:

    from ..cmd.confirm import confirm

    if target.exists():

        if not target.is_dir():
            print(
                "\nDemo target exists but is not a directory:"
                f"\n{target}\n"
            )
            return False

        if any(target.iterdir()):

            if not confirm(
                f"Target directory is not empty: {target}\n"
                "Would you like to continue?"
            ):
                print("\nDemo installation cancelled.\n")
                return False

    target.mkdir(
        parents=True,
        exist_ok=True,
    )

    return True

@roles(Role.FRAMEWORK)
def demo(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True

    framework = context.FRAMEWORK

    wheel = get_distribution(
        outdir=framework.outdir,
    )

    if wheel is None:
        return 1

    target = get_target(
        values=values,
        context=context,
    )

    if dry:
        print(
            "\n"
            f"target: {target}"
            "\n"
            f"dist: {wheel}"
            "\n\n"
            "DRY RUN: No modifications made!"
            "\n"
        )
        return 0

    if not prepare_target(target=target):
        return 0

    from ..environment.runner import run
    from ..environment.upgrade import upgrade
    from ..environment.venv import create_venv
    from ..environment.resolver import resolve_interpreter

    venv_dir = create_venv(target=target / ".venv")

    python = resolve_interpreter(venv_dir)

    result = upgrade(
        python=python,
        cwd=target,
        verbose=verbose,
    )

    if result != 0:
        return 1

    command=[
        str(python),
        "-m",
        "pip",
        "install",
        str(wheel),
    ]

    result = run(
        command=command,
        cwd=target,
        verbose=verbose,
        check=False,
        description="Installing skeleton dist ...",
    )

    if result != 0:
        return 1

    print(
        "wheel installed into demo target: \n"
        f"{target}"
    )

    return 0