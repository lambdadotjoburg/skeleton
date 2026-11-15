import json

from pathlib import Path

from collections.abc import MutableMapping

def format_version(
    version: tuple[int, int, int],
) -> str:

    return ".".join(map(str, version))

def write_pyproject_version(
    pyproject: Path,
    version: tuple[int, int, int],
) -> bool:

    if not pyproject.is_file():
        print(f"Missing Python project file: {pyproject}")
        return False

    try:
        
        import tomlkit

        from tomlkit.exceptions import TOMLKitError

        content = pyproject.read_text(encoding="utf-8")
        configuration = tomlkit.parse(content)

    except (OSError, UnicodeDecodeError, TOMLKitError) as error:

        print(f"Failed to read {pyproject}: {error}")
        return False

    project = configuration.get("project")

    if not isinstance(project, MutableMapping):
        print(f"Missing or invalid [project] section in {pyproject}")
        return False

    project["version"] = format_version(version)

    try:
        pyproject.write_text(
            tomlkit.dumps(configuration),
            encoding="utf-8",
        )

    except OSError as error:

        print(f"Failed to write {pyproject}: {error}")
        return False

    return True

def write_package_version(
    package: Path,
    version: tuple[int, int, int],
) -> bool:

    if not package.is_file():
        print(f"Missing frontend package file: {package}")
        return False

    try:
        with package.open("r", encoding="utf-8") as file:
            configuration = json.load(file)

    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:

        print(f"Failed to read {package}: {error}")
        return False

    if not isinstance(configuration, dict):
        print(f"Invalid package configuration: {package}")
        return False

    configuration["version"] = format_version(version)

    try:
        with package.open("w", encoding="utf-8") as file:

            json.dump(
                configuration,
                file,
                indent=4,
                ensure_ascii=False,
            )

            file.write("\n")

    except OSError as error:

        print(f"Failed to write {package}: {error}")
        return False

    return True