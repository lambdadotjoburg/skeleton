import dataclasses

from typing import Any

from ..runtime.server import ServerName

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class Docs:
    enabled: bool = False
    open: bool
    interface: str | None = None
    url: str

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class PortalService:
    open: bool
    docs: Docs | None

class PortalConfig:

    def __init__(self, data: dict[str, Any]):

        self.browser = data.get("browser", "default")

        services = data["services"]

        docs = data["docs"]

        self.frontend=PortalService(
            **services["frontend"],
            docs=None,
        )

        self.gateway=PortalService(
            **services["gateway"],
            docs=Docs(**docs["gateway"])
        )

        self.backend=PortalService(
            **services["backend"],
            docs=Docs(**docs["backend"])
        )

    @property
    def services(self) -> dict[ServerName, PortalService]:

        return {
            ServerName.FRONTEND: self.frontend,
            ServerName.BACKEND: self.backend,
            ServerName.GATEWAY: self.gateway,
        }

    def service(self,name: ServerName) -> PortalService:
        return self.services[name]
