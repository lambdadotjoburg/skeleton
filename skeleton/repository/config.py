import json, dataclasses

from typing import Any, Iterable

from pathlib import Path

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class Config:

    root: Path

    _cache: dict[Path, dict[str, Any]] = dataclasses.field(
        default_factory=dict,
        init=False,
        repr=False,
        compare=False,
    )

    def paths(
        self,
        pattern: str = "*.json",
        *, 
        exclude: str | Path | tuple[str | Path, ...] | None = None,
    ) -> list[Path]:

        excluded = (
            (exclude,)
            if isinstance(exclude, (str, Path))
            else exclude or ()
        )

        return sorted(
            path
            for path in self.root.glob(pattern)
            if path.is_file()
            and not any(
                path.match(str(pattern))
                for pattern in excluded
            )
        )

    def path(
        self,
        name: str | Path,
        *,
        exists: bool = True,
    ) -> Path:

        path = self.root / name

        if exists and not path.is_file():
            raise ValueError(f"Unknown configuration: {name!r}")

        return path

    def load(
        self,
        name: str | Path,
    ) -> dict[str, Any]:

        path = self.path(name)

        if path not in self._cache:

            with path.open("r", encoding="utf-8") as content:
                data = json.load(content)

            if not isinstance(data, dict):
                raise ValueError(
                    f"Configuration must be a JSON object: {path}"
                )

            object.__setattr__(
                self, "_cache", {
                    **self._cache,
                    path: data,
                },
            )

        return self._cache[path]

    def exists(self, name: str) -> bool:
        return (self.root / name).is_file()

    def require(
        self,
        names: str | Path | Iterable[str | Path],
        *, 
        exclude: str | Path | tuple[str | Path, ...] | None = None,
    ) -> list[Path]:

        names = (
            [names]
            if isinstance(names, (str, Path))
            else list(names)
        )

        excluded = (
            [exclude]
            if isinstance(exclude, (str, Path))
            else list(exclude or ())
        )

        paths = [
            self.path(name, exists=False)
            for name in names
        ]

        paths = [
            path
            for path in paths
            if not any(
                path.match(str(pattern))
                for pattern in excluded
            )
        ]

        missing = [
            path
            for path in paths
            if not path.is_file()
        ]

        if missing:
            raise FileNotFoundError(
                "\n"
                "Required configuration files not found:\n"
                + "\n".join(
                    f"  - {path}"
                    for path in missing
                )
            )

        return paths