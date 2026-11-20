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

        sections: dict[str, Path] = {}

        directory = self.root / "sections"

        if not directory.is_dir():
            return sections

        for path in sorted(directory.iterdir()):

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

    def subsections(
        self,
        *,
        section: str,
    ) -> dict[str, Path]:

        subsections: dict[str, Path] = {}

        directory = self.section(section) / "subsections"

        if not directory.is_dir():
            return subsections

        for path in sorted(directory.iterdir()):

            if not path.is_dir():
                continue

            prefix, separator, name = path.name.partition("-")

            if not separator or not prefix.isdecimal():
                raise ValueError(
                    f"Invalid documentation subsection directory: {path.name!r}"
                )

            if name in subsections:
                raise ValueError(
                    f"Duplicate documentation subsection: {name!r}"
                )

            subsections[name] = path

        return subsections

    def read(
        self,
        *,
        path: Path,
    ) -> str:

        source = path / "index.md"

        return source.read_text(
            encoding="utf-8"
        ).strip()

    def readme(
        self,
        *,
        section: str | None = None,
        subsection: str | None = None,
    ) -> str:

        if subsection is not None and section is None:
            raise ValueError(
                "A subsection requires a section."
            )

        paths: list[Path] = []

        if section is not None:

            paths.append(self.section(section))

            if subsection is not None:

                subsections = self.subsections(section=section)

                if subsection not in subsections:
                    raise ValueError(
                        f"Unknown documentation subsection: {subsection!r}"
                    )

                paths = [subsections[subsection]]

            else:

                paths.extend(
                    self.subsections(section=section).values()
                )

        else:

            for name, path in self.sections.items():

                paths.append(path)

                paths.extend(
                    self.subsections(section=name).values()
                )

        content = []

        for path in paths:
            content.append(self.read(path=path))

        if not content:
            return ""

        return "\n\n".join(content) + "\n"