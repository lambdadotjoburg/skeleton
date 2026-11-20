from __future__ import annotations

import sys

import dataclasses

from pathlib import Path

from typing import Any, override
from typing import TYPE_CHECKING

from .python import PythonLayout
from .boilerplate import ConfigLayout
from .boilerplate import BoilerplateLayout
from ..docs.documentation import Documentation

if TYPE_CHECKING:
    from .client import ClientLayout
    from .engine import EngineLayout

@dataclasses.dataclass(
    kw_only=True,
    frozen=True,
)
class FrameworkLayout(PythonLayout, ConfigLayout):

    root: Path

    CLI: Path = dataclasses.field(init=False)

    DOCUMENTATION: Documentation = dataclasses.field(init=False)

    BOILERPLATE: BoilerplateLayout = dataclasses.field(init=False)

    @property
    def build(self) -> dict[str, Any]:
        return self.config.load(
            "framework.json"
        )["build"]

    @property
    @override
    def main(self) -> Path:
        return  self.root / "run.py"

    @property
    @override
    def venv(self) -> Path:
        return Path(sys.prefix).resolve()

    @property
    def outdir(self) -> Path:
        return self.root / self.build["outdir"]

    @property
    @override
    def venv_python(self) -> Path:
        return Path(sys.executable).resolve()

    def engine(
        self, *, 
        client: ClientLayout,
    ) -> EngineLayout:

        from .engine import EngineLayout
        
        return EngineLayout(
            framework=self,
            client=client,
        )

    def __post_init__(self) -> None:

        super(FrameworkLayout, self).__post_init__()

        object.__setattr__(
            self, "CLI",
            self.root
            / "skeleton"
            / "cli"
            / "definitions"
        )

        object.__setattr__(
            self, "BOILERPLATE",
            BoilerplateLayout(
                root=self.root
                / "skeleton"
                / "boilerplate",
            ),
        )

        object.__setattr__(
            self, "DOCUMENTATION",
            Documentation(
                root=self.root
                / "skeleton"
                / "docs",
            ),
        )

    @property
    def vscode(self) -> Path:
        return self.root / ".vscode" / "settings.json"

    @property
    def artifacts(self) -> list[Path]:

        return [
            path
            for pattern in self.build["artifacts"]
            for path in self.root.glob(pattern)
        ]