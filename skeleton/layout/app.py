import dataclasses

from pathlib import Path

from typing import Literal

from ..repository.manifest import (
    PackageManifest,
    PyProjectManifest,
)

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class AppLayout:

    root: Path

    @property
    def backend(self) -> Path:
        return self.root / "backend"

    @property
    def frontend(self) -> Path:
        return self.root / "frontend"

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
    def package(self) -> Path:
        return self.frontend / "package.json"

    @property
    def index(self) -> Path:
        return self.frontend / "src" / "index.html"

    @property
    def main(self) -> Path:
        return self.backend / "src" / "main.py"

    @property
    def pyproject(self) -> Path:
        return self.backend / "pyproject.toml"

    def manifest(
        self,
        resource: Literal["frontend", "backend"],
    ) -> PackageManifest | PyProjectManifest:

        if resource == "frontend":

            return PackageManifest(path=self.package)

        if resource == "backend":

            return PyProjectManifest(path=self.pyproject)

        raise ValueError("Unsupported manifest resouce type!")