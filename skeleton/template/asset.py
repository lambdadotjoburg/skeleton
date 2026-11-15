import dataclasses

from pathlib import Path

from typing import Iterator

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class Asset:

    source: Path

    destination: Path

    def __iter__(self) -> Iterator[Path]:
        yield self.source
        yield self.destination

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class Template(Asset):

    content: str | bytes | None = None