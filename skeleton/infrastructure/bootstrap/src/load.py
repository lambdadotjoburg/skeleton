import json

from pathlib import Path

def load_layout(path: Path) -> dict[str, str]:

    if not path.is_file():

        raise FileNotFoundError(
            f"Project layout configuration not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        
        config = json.load(file)

    try:

        app = config["project"]["app"]
        frontend = config["frontend"]["directory"]
        backend = config["backend"]["directory"]

    except (KeyError, TypeError) as error:
        raise ValueError(
            f"Invalid project layout configuration: {path}"
        ) from error

    values = {
        "project.app": app,
        "frontend.directory": frontend,
        "backend.directory": backend,
    }

    for key, value in values.items():

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

    return {
        "app": app,
        "frontend": frontend,
        "backend": backend,
    }

# def load_dependencies(path: Path) -> dict:

#     if not path.is_file():
#         raise FileNotFoundError(
#             f"Dependencies configuration not found: {path}"
#         )

#     with path.open(
#         "r",
#         encoding="utf-8",
#     ) as file:
#         config = json.load(file)

#     if not isinstance(config, dict):
#         raise ValueError(
#             f"Invalid dependencies configuration: {path}"
#         )

#     frontend = config.get("frontend")
#     backend = config.get("backend")

#     if not isinstance(frontend, dict):
#         raise ValueError(
#             f"Invalid frontend configuration: {path}"
#         )

#     packages = frontend.get("packages")

#     if not isinstance(packages, dict):
#         raise ValueError(
#             f"Invalid frontend package configuration: {path}"
#         )

#     for group in ("dependencies", "devDependencies"):

#         values = packages.get(group, {})

#         if not isinstance(values, dict):
#             raise ValueError(
#                 f"Invalid frontend '{group}' configuration: {path}"
#             )

#         if not all(
#             isinstance(name, str)
#             and isinstance(version, str)
#             for name, version in values.items()
#         ):
#             raise ValueError(
#                 f"Invalid package entries in frontend '{group}': "
#                 f"{path}"
#             )

#     requirements = (
#         backend.get("requirements")
#         if isinstance(backend, dict)
#         else None
#     )

#     if not isinstance(requirements, list) or not all(
#         isinstance(requirement, str)
#         for requirement in requirements
#     ):
#         raise ValueError(
#             f"Invalid backend requirements configuration: {path}"
#         )

#     return {
#         "frontend": packages,
#         "backend": requirements,
#     }


def load_dependencies(path: Path) -> dict:

    if not path.is_file():
        raise FileNotFoundError(
            f"Dependencies configuration not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = json.load(file)

    if not isinstance(config, dict):
        raise ValueError(
            f"Invalid dependencies configuration: {path}"
        )

    # ---------------------------------------------------------
    # Validate frontend configuration
    # ---------------------------------------------------------

    frontend = config.get("frontend")

    if not isinstance(frontend, dict):
        raise ValueError(
            f"Invalid frontend configuration: {path}"
        )

    packages = frontend.get("packages")

    if not isinstance(packages, dict):
        raise ValueError(
            f"Invalid frontend package configuration: {path}"
        )

    for group in ("dependencies", "devDependencies"):

        values = packages.get(group, {})

        if not isinstance(values, dict):
            raise ValueError(
                f"Invalid frontend '{group}' configuration: {path}"
            )

        if not all(
            isinstance(name, str)
            and name.strip()
            and isinstance(version, str)
            and version.strip()
            for name, version in values.items()
        ):
            raise ValueError(
                f"Invalid package entries in frontend "
                f"'{group}': {path}"
            )

    # ---------------------------------------------------------
    # Validate backend configuration
    # ---------------------------------------------------------

    backend = config.get("backend")

    if not isinstance(backend, dict):
        raise ValueError(
            f"Invalid backend configuration: {path}"
        )

    requirements = backend.get("requirements")

    if not isinstance(requirements, dict):
        raise ValueError(
            f"Invalid backend requirements configuration: "
            f"'backend.requirements' must be an object: {path}"
        )

    if not all(
        isinstance(name, str)
        and name.strip()
        and isinstance(specifier, str)
        and specifier.strip()
        for name, specifier in requirements.items()
    ):
        raise ValueError(
            f"Invalid backend requirements entries: {path}. "
            "Expected package names mapped to non-empty "
            "version specification strings."
        )

    # ---------------------------------------------------------
    # Return the normalized configuration
    # ---------------------------------------------------------

    return {
        "frontend": packages,
        "backend": requirements,
    }