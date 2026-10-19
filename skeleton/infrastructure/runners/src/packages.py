from skeleton.infrastructure.runners.src.command import Command
from skeleton.infrastructure.common.src.context import RuntimeContext
from skeleton.infrastructure.runners.src.utils import resolve_cmd

def start(
    context: RuntimeContext,
    flags: list[str] | None = None
) -> Command:
    
    flags = flags or []

    return Command(
        args=[
            resolve_cmd("npm"),
            "run", "packages:watch",
            *flags
        ],
        cwd=context.root
    )

def build(
    context: RuntimeContext,
    flags: list[str] | None = None
) -> Command:
    
    flags = flags or []
    
    return Command(
        args=[
            resolve_cmd("npm"),
            "run", "packages:build",
            *flags
        ],
        cwd=context.root
    )