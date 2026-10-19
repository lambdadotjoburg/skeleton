from pathlib import Path
from dataclasses import dataclass

from skeleton.infrastructure.common.src.layout import ProjectLayout
from skeleton.infrastructure.common.src.repository import ConfigRepository

@dataclass(frozen=True, kw_only=True)
class RuntimeContext:
    root: Path
    mode: str
    args: list[str]
    env: dict[str, str]
    options: dict[str, str | bool]
    config: ConfigRepository
    layout: ProjectLayout
