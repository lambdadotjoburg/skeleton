import dataclasses

from pathlib import Path

from typing import Any, Literal, TypeAlias

from .config import ConfigLayout
from .backend import BackendLayout
from .frontend import FrontendLayout

from ..runtime.mode import RuntimeMode
from ..runtime.config import RuntimeConfig

Resource: TypeAlias = Literal["frontend", "backend"]

@dataclasses.dataclass(
    frozen=True,
    kw_only=True
)
class ClientLayout(ConfigLayout):
    
    root: Path

    _runtime: RuntimeConfig | None = dataclasses.field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    _frontend: FrontendLayout | None = dataclasses.field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    _backend: BackendLayout | None = dataclasses.field(
        default=None,
        init=False,
        repr=False,
        compare=False,
    )

    @property
    def fastapi(self) -> dict[str, Any]:
        return self.config.load("skeleton-fastapi.json")

    @property
    def metadata(self) -> dict[str, Any]:
        return self.config.load("skeleton-metadata.json")

    @property
    def portal(self) -> dict[str, Any]:
        return self.config.load("skeleton-portal.json")

    @property
    def project(self) -> dict[str, Any]:
        return self.config.load("skeleton-project.json")

    @property
    def proxy(self) -> dict[str, Any]:
        return self.config.load("skeleton-proxy.json")
    
    @property
    def schemas(self) -> dict[str, Any]:
        return self.config.load("skeleton-schemas.json")

    @property
    def servers(self) -> dict[str, Any]:
        return self.config.load("skeleton-servers.json")

    @property
    def dependencies(self) -> dict[str, Any]:
        return self.config.load("skeleton-dependencies.json")

    @property
    def runtime(self) -> RuntimeConfig:

        if self._runtime is None:
            object.__setattr__(
                self,
                "_runtime",
                RuntimeConfig(
                    config=self.config.load(
                        "skeleton-runtime.json"
                    )
                ),
            )

        assert self._runtime is not None
        return self._runtime

    @property
    def mode(self) -> RuntimeMode:
        return self.runtime.mode

    @property
    def profile(self) -> str:
        return self.metadata["profile"]

    @property
    def gitignore(self) -> Path:
        return self.root / ".gitignore"

    @property
    def readme(self) -> Path:
        return self.root / "README.md"

    @property
    def license(self) -> Path:
        return self.root / "LICENSE.md"

    @property
    def frontend(self) -> FrontendLayout:
        if self._frontend is None:
            object.__setattr__(
                self, "_frontend",
                FrontendLayout(client=self)
            )
        assert self._frontend is not None
        return self._frontend

    @property
    def backend(self) -> BackendLayout:
        if self._backend is None:
            object.__setattr__(
                self, "_backend",
                BackendLayout(client=self)
            )
        assert self._backend is not None
        return self._backend

    @property
    def vscode(self) -> Path:
        return self.root / ".vscode" / "settings.json"

    def artifacts(
        self,
        resource: Resource | None = None
    ) -> list[Path]:

        if resource == "frontend":
            return self.frontend.artifacts

        if resource == "backend":
            return self.backend.artifacts

        if resource is None:
            return [
                *self.frontend.artifacts,
                *self.backend.artifacts,
            ]

        raise ValueError(f"Unknown resource: {resource!r}")