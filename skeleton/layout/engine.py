from __future__ import annotations

import dataclasses

from pathlib import Path

from typing import TYPE_CHECKING

from .server import ServerLayout

from ..runtime.reload import ReloadConfig

if TYPE_CHECKING:
    from .client import ClientLayout
    from .framework import FrameworkLayout

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class EngineLayout:

    client: ClientLayout

    framework: FrameworkLayout

    server: ServerLayout = dataclasses.field(init=False,)

    @property
    def root(self) -> Path:
        return (
            self.framework.root
            / "skeleton"
            / "engine"
        )

    def __post_init__(self) -> None:

        object.__setattr__(
            self, "server",
            ServerLayout(
                client=self.client,
                root=(
                    self.framework.root
                    / "skeleton"
                    / "server"
                ),
            ),
        )

    @property
    def reload(self) -> ReloadConfig:
        return ReloadConfig(
            data=self.client.config.load(
                "skeleton-fastapi.json"
            )["reload"]
        )

    @property
    def webpack(self) -> Path:
        return self.client.frontend.webpack