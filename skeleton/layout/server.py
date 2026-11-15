from __future__ import annotations

import dataclasses

from pathlib import Path

from ..runtime.server import Server
from ..runtime.server import ServerName

from ..runtime.proxy import Proxy
from ..runtime.schemas import Schemas

from ..runtime.portal import PortalConfig

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client import ClientLayout

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class ServerLayout:

    root: Path
    
    client: ClientLayout

    @property
    def module(self) -> str:
        return "skeleton.server.main"

    @property
    def servers(self) -> dict[ServerName, Server]:

        return {
            ServerName(name): Server(**config)
            for name, config in self.client.config.load(
                "skeleton-servers.json"
            ).items()
        }

    def server(self,name: ServerName) -> Server:
        return self.servers[name]

    @property
    def proxy(self) -> Proxy:
        return Proxy(
            data = self.client.config.load(
                "skeleton-proxy.json"
            )
        )

    @property
    def portal(self) -> PortalConfig:
        return PortalConfig(
            data=self.client.config.load(
                "skeleton-portal.json"
            )
        )

    @property
    def schemas(self) -> Schemas:
        return Schemas(
            data = self.client.config.load(
                "skeleton-schemas.json"
            )
        )