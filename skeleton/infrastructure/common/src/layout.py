import json

from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ProjectLayout:
    frontend: Path
    backend: Path
    infrastructure: Path
    gateway: Path
    runners: Path
    common: Path
    packages: Path

def build_layout(
    path: Path,
    project_root: Path,
    framework_root: Path,
) -> ProjectLayout:

    if not path.is_file():
        raise FileNotFoundError(
            f"Project layout configuration not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        config = json.load(file)

    try:
        frontend = config["frontend"]["directory"]
        backend = config["backend"]["directory"]

    except (KeyError, TypeError) as error:
        raise ValueError(
            f"Invalid project layout configuration: {path}"
        ) from error

    for key, value in {
        "frontend.directory": frontend,
        "backend.directory": backend,
    }.items():

        if (
            not isinstance(value, str)
            or not value.strip()
            or Path(value).is_absolute()
            or len(Path(value).parts) != 1
            or value in (".", "..")
        ):
            raise ValueError(
                f"Invalid directory name for '{key}': {value!r}"
            )

    project_root = project_root.resolve()
    framework_root = framework_root.resolve()

    infrastructure = framework_root / "skeleton" / "infrastructure"

    return ProjectLayout(
        frontend=project_root / frontend,
        backend=project_root / backend,
        infrastructure=infrastructure,
        gateway=infrastructure / "gateway",
        runners=infrastructure / "runners",
        common=infrastructure / "common",
        packages=framework_root / "skeleton" / "packages",
    )