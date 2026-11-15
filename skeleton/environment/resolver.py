import sys

from pathlib import Path

from typing import Protocol

class Resolver(Protocol):

    def __call__(
        self,
        venv: Path
    ) -> Path: ...

def resolve_interpreter(venv: Path) -> Path:

    import sys
    
    if sys.platform == "win32":
        return venv / "Scripts" / "python.exe"

    return venv / "bin" / "python"

def resolve_module(root: Path, path: Path) -> str:

    return ".".join(    
        path
        .resolve()
        .relative_to(root)
        .with_suffix("").parts
    )

# .venv detection heuristic!
def in_virtual_environment() -> bool:

    return sys.prefix != sys.base_prefix
