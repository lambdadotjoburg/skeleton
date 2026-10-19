from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True, kw_only=True)
class Command:
    args: list[str]
    cwd: Path | None = None