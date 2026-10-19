from skeleton.infrastructure.common.src.constants import Bootstrap
from skeleton.infrastructure.common.src.context import RuntimeContext

from skeleton.infrastructure.runners.src.utils import resolve_cmd
from skeleton.infrastructure.runners.src.command import Command

from skeleton.infrastructure.common.src.utils import (
    resolve_executable_path
)

# def start(
#     context: RuntimeContext,
#     flags: list[str] | None = None
# ) -> Command:

#     flags = flags or []

#     module = Bootstrap.GATEWAY_MODULE

#     framework_root = context.layout.infrastructure.parent.parent

#     python_exe = resolve_executable_path(
#         context.layout.gateway
#     )

#     args = [
#         str(python_exe),
#         "-m", module,
#         "--root", str(context.root),
#         "--mode", str(context.mode),
#     ]

#     if context.options["watch"]:
#         args.append("--watch")

#     if context.options["open"]:
#         args.append("--open")

#     return Command(
#         args=[*args, *flags],
#         cwd=framework_root,
#     )


import sys
from pathlib import Path

from skeleton.infrastructure.common.src.constants import Bootstrap
from skeleton.infrastructure.common.src.context import RuntimeContext
from skeleton.infrastructure.runners.src.utils import resolve_cmd
from skeleton.infrastructure.runners.src.command import Command
from skeleton.infrastructure.common.src.utils import resolve_executable_path


def start(
    context: RuntimeContext,
    flags: list[str] | None = None,
) -> Command:

    flags = flags or []

    module = Bootstrap.GATEWAY_MODULE
    framework_root = context.layout.infrastructure.parent.parent

    # Source-repository development uses its dedicated gateway environment.
    # An installed framework uses the Python environment containing the package.
    if (framework_root / "run.py").is_file():
        python_exe = resolve_executable_path(context.layout.gateway)
    else:
        python_exe = Path(sys.executable)

    args = [
        str(python_exe),
        "-m", module,
        "--root", str(context.root),
        "--mode", str(context.mode),
    ]

    if context.options["watch"]:
        args.append("--watch")

    if context.options["open"]:
        args.append("--open")

    return Command(
        args=[*args, *flags],
        cwd=framework_root,
    )

def build(
    context: RuntimeContext,
    flags: list[str] | None = None
) -> Command:

    flags = flags or []

    return Command(
        args=[
            resolve_cmd("npm"),
            "echo \"Error: no build specified\" && exit 1",
            *flags
        ],
        cwd=context.root
    )