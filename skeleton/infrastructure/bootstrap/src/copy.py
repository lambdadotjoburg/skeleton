import json
import shutil

from pathlib import Path

def copy_template(source: Path, target: Path) -> None:

    target.mkdir(parents=True, exist_ok=True)

    for item in source.iterdir():

        destination = target / item.name

        if destination.exists():

            if item.is_dir() and destination.is_dir():
                copy_template(item, destination)

            continue

        if item.is_dir():
            shutil.copytree(item, destination)

        else:
            shutil.copy2(item, destination)

def _copy_profile_entry_point(
    framework_root: Path,
    project_root: Path,
    frontend: str,
    config: dict,
) -> None:
    """Copy the selected framework's entry point into the client."""

    framework = config.get("framework")

    profile_filenames = {
        "react": "main.tsx",
        "solid": "main.tsx",
        "vue": "main.ts",
    }

    if framework not in profile_filenames:
        raise ValueError(
            f"Unsupported frontend framework: {framework!r}"
        )

    entry = config.get("entry")
    if not isinstance(entry, dict):
        raise ValueError(
            "skeleton-config.json: 'entry' must be an object."
        )

    entry_name = entry.get("main")
    if not isinstance(entry_name, str) or not entry_name.strip():
        raise ValueError(
            "skeleton-config.json: 'entry.main' must be "
            "a non-empty string."
        )

    source_name = profile_filenames[framework]

    source = (
        framework_root
        / "skeleton"
        / "infrastructure"
        / "bootstrap"
        / "src"
        / "templates"
        / "profiles"
        / framework
        / source_name
    )

    if not source.is_file():
        raise FileNotFoundError(
            f"Frontend entry-point template not found: {source}"
        )

    # entry.main is relative to the frontend source directory.
    entry_path = Path(entry_name)

    if entry_path.is_absolute() or ".." in entry_path.parts:
        raise ValueError(
            "skeleton-config.json: 'entry.main' must be a "
            "relative path within the frontend source directory."
        )

    # If an extension is supplied, it must match the selected profile.
    if entry_path.suffix and entry_path.suffix != source.suffix:
        raise ValueError(
            f"Entry point {entry_name!r} must use the "
            f"{source.suffix} extension for {framework}."
        )

    if not entry_path.suffix:
        entry_path = entry_path.with_suffix(source.suffix)

    config_lib = config.get("lib")
    if not isinstance(config_lib, dict):
        raise ValueError(
            "skeleton-config.json: 'lib' must be an object."
        )

    source_directory = config_lib.get("src", "src")
    if (
        not isinstance(source_directory, str)
        or not source_directory.strip()
    ):
        raise ValueError(
            "skeleton-config.json: 'lib.src' must be "
            "a non-empty relative path."
        )

    source_path = Path(source_directory)
    if source_path.is_absolute() or ".." in source_path.parts:
        raise ValueError(
            "skeleton-config.json: 'lib.src' must be a "
            "relative path within the frontend directory."
        )

    frontend_root = project_root / frontend
    if not frontend_root.is_dir():
        raise FileNotFoundError(
            f"Frontend directory not found: {frontend_root}"
        )

    destination_directory = frontend_root / source_path
    destination = destination_directory / entry_path

    # Preserve existing client code on repeated initialization.
    if destination.exists():
        print(
            f"INFO: Preserving existing frontend entry point: "
            f"{destination}"
        )
        return

    destination_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    shutil.copy2(source, destination)

    print(
        f"INFO: Copied {framework} entry point: {destination}"
    )

def _copy_profile_files(
    framework_root: Path,
    project_root: Path,
    frontend: str,
    config: dict,
) -> None:
    """Copy additional source files required by the selected framework."""

    framework = config.get("framework")

    profile_files = {
        "react": (),
        "solid": (),
        "vue": (
            "App.vue",
            "vue.d.ts",
        ),
    }

    if framework not in profile_files:
        raise ValueError(
            f"Unsupported frontend framework: {framework!r}"
        )

    if not profile_files[framework]:
        return

    config_lib = config.get("lib")

    if not isinstance(config_lib, dict):
        raise ValueError(
            "skeleton-config.json: 'lib' must be an object."
        )

    source_directory = config_lib.get("src", "src")

    if (
        not isinstance(source_directory, str)
        or not source_directory.strip()
    ):
        raise ValueError(
            "skeleton-config.json: 'lib.src' must be "
            "a non-empty relative path."
        )

    source_path = Path(source_directory)

    if source_path.is_absolute() or ".." in source_path.parts:
        raise ValueError(
            "skeleton-config.json: 'lib.src' must be a "
            "relative path within the frontend directory."
        )

    profile = (
        framework_root
        / "skeleton"
        / "infrastructure"
        / "bootstrap"
        / "src"
        / "templates"
        / "profiles"
        / framework
    )

    destination_directory = (
        project_root
        / frontend
        / source_path
    )

    destination_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    for filename in profile_files[framework]:

        source = profile / filename
        destination = destination_directory / filename

        if not source.is_file():
            raise FileNotFoundError(
                f"Frontend profile template not found: {source}"
            )

        # Preserve client files on repeated initialization.
        if destination.exists():
            print(
                f"INFO: Preserving existing frontend file: "
                f"{destination}"
            )
            continue

        shutil.copy2(
            source,
            destination,
        )

        print(
            f"INFO: Copied {framework} profile file: "
            f"{destination}"
        )

def copy_app_template(
    source: Path,
    target: Path,
    frontend: str,
    backend: str,
    framework_root: Path,
) -> None:

    target.mkdir(parents=True, exist_ok=True)

    directories = {
        "frontend": frontend,
        "backend": backend,
    }

    # ---------------------------------------------------------
    # Copy the application templates.
    # ---------------------------------------------------------

    for item in source.iterdir():

        name = directories.get(item.name, item.name)
        destination = target / name

        if destination.exists():

            if item.is_dir() and destination.is_dir():
                copy_template(item, destination)

            continue

        if item.is_dir():
            shutil.copytree(item, destination)

        else:
            shutil.copy2(item, destination)

    # ---------------------------------------------------------
    # Read the selected frontend framework.
    # ---------------------------------------------------------

    config_path = target / "skeleton-config.json"

    if not config_path.is_file():
        raise FileNotFoundError(
            f"Skeleton configuration not found: {config_path}. "
            "Run 'skeleton --config' first."
        )

    with config_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = json.load(file)

    if not isinstance(config, dict):
        raise ValueError(
            f"Expected a JSON object: {config_path}"
        )

    framework = config.get("framework")

    supported_frameworks = {
        "react",
        "solid",
        "vue",
    }

    if framework not in supported_frameworks:
        raise ValueError(
            f"Unsupported frontend framework in {config_path}: "
            f"{framework!r}. Choose one of: "
            f"{', '.join(sorted(supported_frameworks))}"
        )

    # ---------------------------------------------------------
    # Locate the selected profile's TypeScript configuration.
    # ---------------------------------------------------------

    profile_tsconfig = (
        framework_root
        / "skeleton"
        / "infrastructure"
        / "bootstrap"
        / "src"
        / "templates"
        / "profiles"
        / framework
        / "tsconfig.json"
    )

    if not profile_tsconfig.is_file():
        raise FileNotFoundError(
            f"TypeScript configuration not found for "
            f"framework {framework!r}: {profile_tsconfig}"
        )

    # ---------------------------------------------------------
    # Copy tsconfig.json into the configured frontend directory.
    # ---------------------------------------------------------

    frontend_root = target / frontend

    if not frontend_root.is_dir():
        raise FileNotFoundError(
            f"Frontend directory not found: {frontend_root}"
        )

    destination = frontend_root / "tsconfig.json"

    shutil.copy2(
        profile_tsconfig,
        destination,
    )

    print(
        f"INFO: Copied {framework} TypeScript configuration: "
        f"{destination}"
    )

    # ---------------------------------------------------------
    # Copy the selected profile's entry point.
    # ---------------------------------------------------------

    _copy_profile_entry_point(
        framework_root=framework_root,
        project_root=target,
        frontend=frontend,
        config=config,
    )

    # ---------------------------------------------------------
    # Copy additional framework-specific source files.
    # ---------------------------------------------------------

    _copy_profile_files(
        framework_root=framework_root,
        project_root=target,
        frontend=frontend,
        config=config,
    )