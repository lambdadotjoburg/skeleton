import dataclasses

from pathlib import Path

from .app import AppLayout
from .config import ConfigLayout
from .profile import ProfileLayout
from .config import VSCodeLayout

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class BoilerplateLayout(ConfigLayout):

    root: Path

    PROFILES: Path = dataclasses.field(
        init=False,
        repr=False,
    )

    PLUGINS: Path = dataclasses.field(
        init=False,
        repr=False,
    )

    APP: AppLayout = dataclasses.field(
        init=False,
        repr=False,
    )

    VSCODE: VSCodeLayout = dataclasses.field(
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        
        super().__post_init__()

        object.__setattr__(
            self, "PROFILES",
            self.root / "profiles",
        )

        object.__setattr__(
            self, "PLUGINS",
            self.root / "plugins",
        )

        object.__setattr__(
            self, "APP",
            AppLayout(root=self.root / "app"),
        )

        object.__setattr__(
            self, "VSCODE",
            VSCodeLayout(root = self.root),
        )

    @property
    def app(self) -> AppLayout:
        return self.APP

    @property
    def vscode(self) -> VSCodeLayout:
        return self.VSCODE

    @property
    def profiles(self) -> dict[str, ProfileLayout]:

        return {
            path.name: ProfileLayout(root=path)
            for path in self.PROFILES.iterdir()
            if path.is_dir()
        }

    def profile(self, name: str) -> ProfileLayout:

        path = self.PROFILES / name

        if not path.is_dir():
            raise ValueError(
                f"Unknown client profile: {name!r}"
            )

        return ProfileLayout(root=path)

    def extension(self, profile: str) -> str:
        return self.profile(profile).extension