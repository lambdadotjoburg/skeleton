from __future__ import annotations

import dataclasses

from pathlib import Path

from typing import Any, override
from typing import TYPE_CHECKING

from skeleton.layout.python import PythonLayout

if TYPE_CHECKING:
    from .client import ClientLayout

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class BackendLayout(PythonLayout):

    client: ClientLayout

    @property
    def project(self) -> dict[str, Any]:
        return self.client.project["backend"]

    @property
    def dir(self) -> str:
        return self.project["dir"]

    @property
    @override
    def root(self) -> Path:
        return self.client.root / self.dir

    # type trick!
    @root.setter
    def root(self, _: Path) -> None:
        pass

    @property
    def lib(self) -> dict[str, str]:
        return self.project["lib"]

    @property
    def build(self) -> dict[str, Any]:
        return self.project["build"]

    @property
    def config(self) -> dict[str, str]:
        return self.project["config"]

    # lib info:

    @property
    def src(self) -> Path:
        return self.root / self.lib["src"]

    @property
    @override
    def main(self) -> Path:
        return self.src / f"{self.lib['main']}.py"

    @property
    @override
    def module(self) -> str:
        return ".".join(
            (
                *self.src.relative_to(self.root).parts,
                self.main.stem,
            )
        )

    @property
    def app(self) -> str:
        return self.lib["app"]

    @property
    def entry(self) -> str:
        return f"{self.module}:{self.lib["app"]}"

    # environment info:

    @property
    @override
    def venv(self) -> Path:
        return self.root / self.project["venv"]

    # build info:

    @property
    def outdir(self) -> Path:
        return self.root / self.build["outdir"]

    @property
    def artifacts(self) -> list[Path]:
        return [
            path
            for pattern in self.build["artifacts"]
            for path in self.root.glob(pattern)
        ]

    # config info:

    @property
    @override
    def pyproject(self) -> Path:
        return self.root / self.config["pyproject"]
