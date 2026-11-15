import json

import tomllib

from pathlib import Path

from .parse import parse_version

def read_pyproject_version(
    pyproject: Path,
) -> tuple[int, int, int] | None:

    if not pyproject.is_file():
        print(f"Missing Python project file: {pyproject}")
        return None

    try:
        with pyproject.open("rb") as file:
            configuration = tomllib.load(file)

    except (OSError, tomllib.TOMLDecodeError) as error:
        print(f"Failed to read {pyproject}: {error}")
        return None

    metadata = configuration.get("project")

    if not isinstance(metadata, dict):
        print(f"Missing [project] section in {pyproject}")
        return None

    version = metadata.get("version")

    if not isinstance(version, str):
        print(f"Missing or invalid project.version in {pyproject}")
        return None

    parsed = parse_version(version)

    if parsed is None:
        print(
            f"Invalid version '{version}' in {pyproject}. "
            "Expected MAJOR.MINOR.PATCH."
        )

    return parsed

def read_package_version(
    package: Path,
) -> tuple[int, int, int] | None:

    if not package.is_file():
        print(f"Missing frontend package file: {package}")
        return None

    try:
        with package.open("r", encoding="utf-8") as file:
            configuration = json.load(file)

    except (OSError, json.JSONDecodeError) as error:
        print(f"Failed to read {package}: {error}")
        return None

    if not isinstance(configuration, dict):
        print(f"Invalid package configuration: {package}")
        return None

    version = configuration.get("version")

    if not isinstance(version, str):
        print(f"Missing or invalid version in {package}")
        return None

    parsed = parse_version(version)

    if parsed is None:
        print(
            f"Invalid version '{version}' in {package}. "
            "Expected MAJOR.MINOR.PATCH."
        )

    return parsed
