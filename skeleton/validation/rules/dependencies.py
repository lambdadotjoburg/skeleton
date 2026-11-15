import re

from typing import Any

from collections.abc import Mapping

from packaging.requirements import Requirement

NPM_NAME = re.compile(
    r"(?:@[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?/)?"
    r"[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?"
)

def npm_dependencies(value: Any) -> str | None:

    return validate_dependency_group(
        value=value,
        ecosystem="npm",
    )

def python_dependencies(value: Any) -> str | None:

    return validate_dependency_group(
        value=value,
        ecosystem="python",
    )

def validate_dependency_group(
    *,
    value: Any,
    ecosystem: str,
) -> str | None:

    if not isinstance(value, Mapping):
        return "Expected a dependency configuration object."

    errors: list[str] = []

    expected = {
        "dependencies",
        "devDependencies",
    }

    for name in value:

        if name not in expected:
            errors.append(f"Unsupported dependency group: {name}")

    for group in expected:

        if group not in value:
            errors.append(f"Missing dependency group: {group}")
            continue

        packages = value[group]

        if not isinstance(packages, Mapping):
            errors.append(
                f"{group}: Expected an object of package names and versions."
            )
            continue

        for name, version in packages.items():

            if not isinstance(name, str) or not name:
                errors.append(f"{group}: Invalid package name: {name!r}")
                continue

            if not isinstance(version, str) or not version.strip():
                errors.append(
                    f"{group}.{name}: Expected a non-empty version expression."
                )
                continue

            if ecosystem == "npm":

                if len(name) > 214 or NPM_NAME.fullmatch(name) is None:
                    errors.append(
                        f"{group}.{name}: Invalid npm package name."
                    )
                    continue

                try:
                    import anyver

                    anyver.range_contains(
                        "0.0.0",
                        version,
                        ecosystem="npm",
                    )

                except ValueError:
                    errors.append(
                        f"{group}.{name}: Invalid npm version range: {version!r}"
                    )

            elif ecosystem == "python":

                try:
                    requirement = Requirement(f"{name}{version}")

                    if (
                        requirement.url is not None
                        or requirement.marker is not None
                        or requirement.extras
                        or not str(requirement.specifier)
                    ):
                        raise ValueError

                except (ValueError, TypeError):
                    errors.append(
                        f"{group}.{name}: Invalid Python version specifier: "
                        f"{version!r}"
                    )

    if errors:
        return "\n".join(errors)

    return None
