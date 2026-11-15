from __future__ import annotations

import dataclasses

from pathlib import Path

from typing import TYPE_CHECKING

from .mode import Mode

from ..cmd.registry import CommandRegistry

if TYPE_CHECKING:
    from ..layout.framework import FrameworkLayout

@dataclasses.dataclass(
    kw_only=True,
    frozen=True,
)
class CLIContext:

    cwd: Path
    root: Path
    
    REGISTRY: CommandRegistry
    FRAMEWORK: FrameworkLayout

    @property
    def mode(self) -> Mode:
        if self.cwd == self.FRAMEWORK.root:
            return Mode.FRAMEWORK
        return Mode.CLIENT
