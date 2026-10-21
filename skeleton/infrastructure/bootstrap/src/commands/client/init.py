import json
import os
import re
import shutil

from pathlib import Path

from skeleton.infrastructure.bootstrap.src.copy import (
    copy_app_template,
)

from skeleton.infrastructure.bootstrap.src.load import (
    load_dependencies,
    load_layout,
)

CLIENT_REQUIREMENTS_MARKER = (
    "# --- Skeleton client dependencies (managed) ---"
)

def _requirement_name(requirement: str) -> str | None:

    requirement = requirement.strip()

    if not requirement or requirement.startswith("#"):
        return None

    match = re.match(
        r"^([A-Za-z0-9][A-Za-z0-9._-]*)",
        requirement,
    )

    if not match:
        return None

    return re.sub(
        r"[-_.]+",
        "-",
        match.group(1),
    ).lower()

def _merge_backend_requirements(
    requirements: Path,
    client_packages: dict[str, str],
) -> None:

    if not requirements.is_file():
        raise FileNotFoundError(
            f"Backend template requirements not found: {requirements}"
        )

    if not isinstance(client_packages, dict):
        raise ValueError(
            "skeleton-dependencies.json: "
            "'backend.requirements' must be an object mapping "
            "package names to version specifications."
        )

    lines = requirements.read_text(
        encoding="utf-8",
    ).splitlines()

    # ---------------------------------------------------------
    # Remove the previously generated client section
    # ---------------------------------------------------------

    try:
        marker_index = lines.index(
            CLIENT_REQUIREMENTS_MARKER
        )
        base_lines = lines[:marker_index]

    except ValueError:
        base_lines = lines

    # ---------------------------------------------------------
    # Identify packages already required by the template
    # ---------------------------------------------------------

    existing_names = {
        name
        for line in base_lines
        if (
            name := _requirement_name(line)
        ) is not None
    }

    # ---------------------------------------------------------
    # Build the managed client requirements
    # ---------------------------------------------------------

    client_lines: list[str] = []
    client_names: set[str] = set()

    package_pattern = re.compile(
        r"^[A-Za-z0-9][A-Za-z0-9._-]*$"
    )

    for package, specifier in client_packages.items():

        # Validate the package name.
        if (
            not isinstance(package, str)
            or not package_pattern.fullmatch(package)
        ):
            raise ValueError(
                f"Invalid Python package name: {package!r}"
            )

        # Validate the version specification.
        if (
            not isinstance(specifier, str)
            or not specifier.strip()
        ):
            raise ValueError(
                f"Invalid version specification for "
                f"{package!r}: {specifier!r}. "
                "Use a non-empty PEP 440 version specification, "
                "such as '>=2.0,<3.0' or '==2.1.0'."
            )

        specifier = specifier.strip()

        if not re.match(
            r"^(===|~=|==|!=|<=|>=|<|>)",
            specifier,
        ):
            raise ValueError(
                f"Invalid version specification for "
                f"{package!r}: {specifier!r}. "
                "Expected a version constraint such as "
                "'>=2.0,<3.0' or '==2.1.0'."
            )

        name = re.sub(
            r"[-_.]+",
            "-",
            package,
        ).lower()

        # Reject duplicate names with different capitalization
        # or punctuation, e.g. SQLAlchemy and sqlalchemy.
        if name in client_names:
            raise ValueError(
                f"Duplicate backend dependency: {package!r}"
            )

        client_names.add(name)

        # Do not silently ignore a client's version constraint
        # when the template already declares the same package.
        if name in existing_names:
            raise ValueError(
                f"Backend dependency conflict for {package!r}: "
                "the package is already declared in the backend "
                "template requirements. Reconcile the template "
                "and client configuration before initialization."
            )

        client_lines.append(
            f"{package}{specifier}"
        )

    # ---------------------------------------------------------
    # Rebuild requirements.txt
    # ---------------------------------------------------------

    while base_lines and not base_lines[-1].strip():
        base_lines.pop()

    merged_lines = list(base_lines)

    if client_lines:

        if merged_lines:
            merged_lines.append("")

        merged_lines.append(
            CLIENT_REQUIREMENTS_MARKER
        )
        merged_lines.extend(client_lines)

    requirements.write_text(
        "\n".join(merged_lines) + "\n",
        encoding="utf-8",
    )

def _merge_frontend_dependencies(
    package_json: Path,
    frontend_config: dict,
    tarballs: dict[str, Path],
    frontend_root: Path,
) -> None:

    if not package_json.is_file():
        raise FileNotFoundError(
            f"Frontend package manifest not found: {package_json}"
        )

    # ---------------------------------------------------------
    # Load the frontend package manifest
    # ---------------------------------------------------------

    with package_json.open(
        "r",
        encoding="utf-8",
    ) as file:
        package = json.load(file)

    # ---------------------------------------------------------
    # Read configured dependency groups
    # ---------------------------------------------------------

    configured_dependencies = frontend_config.get(
        "dependencies",
        {},
    )

    configured_dev_dependencies = frontend_config.get(
        "devDependencies",
        {},
    )

    if not isinstance(configured_dependencies, dict):
        raise ValueError(
            "skeleton-dependencies.json: "
            "'frontend.packages.dependencies' must be an object."
        )

    if not isinstance(configured_dev_dependencies, dict):
        raise ValueError(
            "skeleton-dependencies.json: "
            "'frontend.packages.devDependencies' must be an object."
        )

    duplicates = (
        configured_dependencies.keys()
        & configured_dev_dependencies.keys()
    )

    if duplicates:
        names = ", ".join(sorted(duplicates))
        raise ValueError(
            "Frontend packages cannot be declared in both "
            f"'dependencies' and 'devDependencies': {names}"
        )

    # ---------------------------------------------------------
    # Get the package manifest dependency sections
    # ---------------------------------------------------------

    dependencies = package.setdefault(
        "dependencies",
        {},
    )

    dev_dependencies = package.setdefault(
        "devDependencies",
        {},
    )

    if not isinstance(dependencies, dict):
        raise ValueError(
            f"'dependencies' must be an object in {package_json}"
        )

    if not isinstance(dev_dependencies, dict):
        raise ValueError(
            f"'devDependencies' must be an object in {package_json}"
        )

    # ---------------------------------------------------------
    # Reconcile configured application dependencies
    # ---------------------------------------------------------

    for name in (
        configured_dependencies.keys()
        | configured_dev_dependencies.keys()
    ):

        # Remove any previous declaration from either group.
        dependencies.pop(name, None)
        dev_dependencies.pop(name, None)

    dependencies.update(configured_dependencies)
    dev_dependencies.update(configured_dev_dependencies)

    # ---------------------------------------------------------
    # Configure local Skeleton package tarballs
    # ---------------------------------------------------------

    for package_name, source_tarball in tarballs.items():

        # Skeleton tooling belongs in devDependencies.
        dependencies.pop(package_name, None)

        relative_path = Path(
            os.path.relpath(
                source_tarball,
                frontend_root,
            )
        ).as_posix()

        dev_dependencies[package_name] = (
            f"file:{relative_path}"
        )

    # ---------------------------------------------------------
    # Write the reconciled frontend package manifest
    # ---------------------------------------------------------

    with package_json.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            package,
            file,
            indent=4,
        )
        file.write("\n")

def init(
    framework_root: Path,
    project_root: Path,
) -> None:

    framework_root = framework_root.resolve()
    project_root = project_root.resolve()

    templates = (
        framework_root
        / "skeleton"
        / "infrastructure"
        / "bootstrap"
        / "src"
        / "templates"
        / "app"
    )

    if not templates.is_dir():
        raise FileNotFoundError(
            f"Application templates not found: {templates}"
        )

    layout = load_layout(
        project_root / "skeleton-layout.json"
    )

    dependencies = load_dependencies(
        project_root / "skeleton-dependencies.json"
    )

    print(f"INFO: Initializing project: {project_root}")

    # ---------------------------------------------------------
    # Copy the application template
    # ---------------------------------------------------------

    copy_app_template(
        source=templates,
        target=project_root,
        frontend=layout["frontend"],
        backend=layout["backend"],
        framework_root=framework_root,
    )

    # ---------------------------------------------------------
    # Merge the configured client backend dependencies
    # ---------------------------------------------------------

    requirements = (
        project_root
        / layout["backend"]
        / "requirements.txt"
    )

    _merge_backend_requirements(
        requirements,
        dependencies["backend"],
    )

    print(
        f"INFO: Generated backend requirements: {requirements}"
    )

    # ---------------------------------------------------------
    # Locate the prepared Skeleton tooling packages
    # ---------------------------------------------------------

    source = (
        framework_root
        / "skeleton"
        / "packages"
        / ".skeleton"
    )

    if not source.is_dir():
        raise FileNotFoundError(
            f"Packaged Skeleton artifacts not found: {source}\n"
            "Run 'python run.py --dev-pack' in the framework "
            "repository before initializing the client."
        )

    package_prefixes = (
        "skeleton-cli",
        "skeleton-webpack",
    )

    tarballs: list[Path] = []

    for prefix in package_prefixes:

        matches = sorted(
            source.glob(f"{prefix}-*.tgz")
        )

        if len(matches) != 1:
            raise FileNotFoundError(
                f"Expected exactly one {prefix} tarball in "
                f"{source}, but found {len(matches)}."
            )

        tarballs.append(matches[0])

    # ---------------------------------------------------------
    # Copy prepared tarballs into the client project
    # ---------------------------------------------------------

    destination = (
        project_root
        / ".skeleton"
        / "packages"
    )

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Remove outdated copies of these packages only.
    for prefix in package_prefixes:

        for old_tarball in destination.glob(
            f"{prefix}-*.tgz"
        ):
            old_tarball.unlink()

    for tarball in tarballs:

        shutil.copy2(
            tarball,
            destination / tarball.name,
        )

    print(
        f"INFO: Copied Skeleton packages to {destination}"
    )

    # ---------------------------------------------------------
    # Reconcile the frontend package manifest
    # ---------------------------------------------------------

    frontend_root = project_root / layout["frontend"]
    package_json = frontend_root / "package.json"

    local_tarballs = {
        "@skeleton/cli": (
            destination / tarballs[0].name
        ).resolve(),
        "@skeleton/webpack": (
            destination / tarballs[1].name
        ).resolve(),
    }

    _merge_frontend_dependencies(
        package_json=package_json,
        frontend_config=dependencies["frontend"],
        tarballs=local_tarballs,
        frontend_root=frontend_root,
    )

    print(
        f"INFO: Reconciled frontend dependencies: {package_json}"
    )

    print("INFO: Project initialization complete")
