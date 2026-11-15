import dataclasses

from pathlib import Path

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class Documentation:

    root: Path

    @property
    def sections(self) -> dict[str, Path]:

        sections = {}

        for path in sorted(
            (
                self.root
                / "sections"
            ).iterdir()
        ):

            if not path.is_dir():
                continue

            prefix, separator, name = path.name.partition("-")

            if not separator or not prefix.isdecimal():
                raise ValueError(
                    f"Invalid documentation section directory: {path.name!r}"
                )

            if name in sections:
                raise ValueError(
                    f"Duplicate documentation section: {name!r}"
                )

            sections[name] = path

        return sections

    def section(self, name: str) -> Path:

        sections = self.sections

        if name not in sections:
            raise ValueError(
                f"Unknown documentation section: {name!r}"
            )

        return sections[name]

    def readme(
        self,
        *,
        section: str | None = None,
    ) -> str:

        if section is not None:
            paths = [self.section(section)]
        else:
            paths = self.sections.values()

        content = []

        for path in paths:

            source = path / "index.md"

            content.append(
                source.read_text(
                    encoding="utf-8"
                ).strip()
            )

        return "\n\n".join(content) + "\n"