import dataclasses

from pathlib import Path

from ..repository.config import Config

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class ConfigLayout:

    root: Path

    _config: Config = dataclasses.field(
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "_config",
            Config(root=self.root / "config"),
        )

    @property
    def config(self) -> Config:
        return self._config

class VSCodeLayout(ConfigLayout):

    def __post_init__(self) -> None:

        super().__post_init__()

        object.__setattr__(

            self, "_config",
            Config(root=self.root / ".vscode"),
        )
        