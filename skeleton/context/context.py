from __future__ import annotations

import dataclasses

from pathlib import Path

from typing import TYPE_CHECKING

from .mode import Mode

from ..cmd.registry import CommandRegistry

if TYPE_CHECKING:
    from ..layout.client import ClientLayout
    from ..layout.framework import FrameworkLayout

@dataclasses.dataclass(
    kw_only=True,
    frozen=True,
)
class CLIContext:

    cwd: Path
    root: Path

    CLIENT: ClientLayout | None
    FRAMEWORK: FrameworkLayout

    _registry: CommandRegistry | None = dataclasses.field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:

        from .auth import Authorization
        from .predicates import predicates

        registry = CommandRegistry(
            context=self,
            authorizer=Authorization(
                context=self,
                predicates=predicates,
            )
        )

        object.__setattr__(
            self,
            "_registry",
            registry,
        )

    @property
    def REGISTRY(self) -> CommandRegistry:
        return self._registry
    
    @property
    def mode(self) -> Mode:
        if self.cwd == self.FRAMEWORK.root:
            return Mode.FRAMEWORK
        return Mode.CLIENT
