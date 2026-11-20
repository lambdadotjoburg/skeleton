from pathlib import Path

REGEX_DEPENDENCIES = r"\s*([A-Za-z0-9][A-Za-z0-9._-]*)"

def require(root: Path, *, dev: bool = False) -> set[str]:

    import re, tomllib

    path = root / "pyproject.toml"

    with path.open("rb") as file:
        project = tomllib.load(file)["project"]

    dependencies = list(project.get("dependencies", []))

    if dev:
        dependencies.extend(
            project.get("optional-dependencies", {}).get("dev", [])
        )

    required = set()

    for dependency in dependencies:

        match = re.match(REGEX_DEPENDENCIES, dependency)

        if match is None:
            raise ValueError(
                f"Invalid dependency declaration: {dependency!r}"
            )

        required.add(match.group(1))

    return required

def dependencies(root: Path, *, dev: bool = False) -> list[str]:

    from importlib.metadata import version

    from importlib.metadata import PackageNotFoundError

    missing = []

    for dependency in sorted(require(root, dev=dev)):
        
        try:
            version(dependency)

        except PackageNotFoundError:

            missing.append(dependency)

    return missing