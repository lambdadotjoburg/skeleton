import re

from typing import Any, Mapping

def merge_dependencies(
    declared: list[str],
    configured: Mapping[str, str],
) -> None:

    positions: dict[str, int] = {}

    # Index existing dependencies by normalized package name.
    for position, requirement in enumerate(declared):

        match = re.match(
            r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)",
            requirement,
        )

        if match is None:
            raise ValueError(
                f"Invalid project dependency: {requirement!r}"
            )

        name = re.sub(
            r"[-_.]+",
            "-",
            match.group(1),
        ).lower()

        positions[name] = position

    # Add or replace configured dependencies.
    for name, version in configured.items():

        key = re.sub(
            r"[-_.]+",
            "-",
            name,
        ).lower()

        requirement = f"{name}{version}"

        if key in positions:

            declared[positions[key]] = requirement

        else:

            positions[key] = len(declared)
            declared.append(requirement)

def merge_package_dependencies(
    package: dict[str, Any],
    dependencies: Mapping[str, Mapping[str, str]],
) -> dict[str, Any]:

    package.setdefault("dependencies", {}).update(
        dependencies["dependencies"]
    )

    package.setdefault("devDependencies", {}).update(
        dependencies["devDependencies"]
    )

    return package

def merge_pyproject_dependencies(
    pyproject: str,
    dependencies: Mapping[str, Mapping[str, str]],
) -> str:

    import tomlkit

    document = tomlkit.parse(pyproject)

    project = document["project"]

    merge_dependencies(
        project["dependencies"],
        dependencies["dependencies"],
    )

    merge_dependencies(
        project["optional-dependencies"]["dev"],
        dependencies["devDependencies"],
    )

    return tomlkit.dumps(document)
