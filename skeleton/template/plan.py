import dataclasses

from pathlib import Path

from typing import Iterator

from .asset import Asset, Template

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class ProjectPlan:

    root: Path

    folders: list[Asset]

    files: list[Asset]

    templates: list[Template]

    def __iter__(self) -> Iterator[Asset]:
        yield from self.folders
        yield from self.files
        yield from self.templates
