from __future__ import annotations

import shutil

import dataclasses

from pathlib import Path

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .client import ClientLayout

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class FrontendLayout:

    client: ClientLayout

    @property
    def project(self) -> dict[str, Any]:
        return self.client.project["frontend"]

    @property
    def dir(self) -> str:
        return self.project["dir"]

    @property
    def root(self) -> Path:
        return self.client.root / self.dir

    @property
    def webpack(self) -> Path:
        return self.root / self.project["webpack"]

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

    def main(self, extension: str) -> Path:
        return self.src / f"{self.lib['main']}.{extension.lstrip('.')}"

    @property
    def index(self) -> Path:
        return self.src / f"{self.lib['index']}.html"

    @property
    def static(self) -> Path:
        return self.src / self.lib["static"]

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
    def tsconfig(self) -> Path:
        return self.root / self.config["tsconfig"]

    @property
    def package(self) -> Path:
        return self.root / self.config["package"]

    @property
    def npm(self) -> str:
        
        # npm = "npm.cmd" if os.name == "nt" else "npm"

        # gets npm from ENV vars!
        npm = shutil.which("npm")

        if npm is None:
            raise FileNotFoundError(
                "npm was not found:\n"
                "Install Node.js & npm first!"
            )

        return npm
