import dataclasses

from pathlib import Path
from typing import Any

from .config import ConfigLayout

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class ProfileLayout(ConfigLayout):
    root: Path

    @property
    def name(self) -> str:
        return self.root.name

    @property
    def frontend(self) -> Path:
        return self.root / "frontend"

    @property
    def webpack(self) -> Path:
        return self.frontend / "webpack.config.js"

    @property
    def tsconfig(self) -> Path:
        return self.frontend / "tsconfig.json"

    @property
    def dependencies(self) -> dict[str, Any]:
        return self.config.load(
            "skeleton-dependencies.json"
        )

    @property
    def extension(self) -> str:
        return self.main.suffix.lstrip(".")

    @property
    def main(self) -> Path:

        files = list((self.frontend / "src").glob("main.*"))

        if len(files) != 1:
            raise ValueError(
                f"Expected exactly one main file in: "
                f"{self.frontend / 'src'}"
            )
        
        return files[0]