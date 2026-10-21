import json, shutil
from pathlib import Path

SUPPORTED_FRAMEWORKS = {"react", "solid", "vue"}

def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object: {path}")

    return data

def write_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        file.write("\n")

def config(
    framework_root: Path,
    project_root: Path,
    framework: str | None = None,
) -> None:

    templates_root = (
        framework_root
        / "skeleton"
        / "infrastructure"
        / "bootstrap"
        / "src"
        / "templates"
    )

    config_templates = templates_root / "config"
    profiles_root = templates_root / "profiles"

    if not config_templates.is_dir():
        raise FileNotFoundError(
            f"Configuration templates not found: {config_templates}"
        )

    if not profiles_root.is_dir():
        raise FileNotFoundError(
            f"Framework profiles not found: {profiles_root}"
        )

    if framework is not None:
        framework = framework.strip().lower()

        if framework not in SUPPORTED_FRAMEWORKS:
            supported = ", ".join(sorted(SUPPORTED_FRAMEWORKS))
            raise ValueError(
                f"Unsupported frontend framework: {framework!r}. "
                f"Choose one of: {supported}"
            )

    project_root = project_root.resolve()
    project_root.mkdir(parents=True, exist_ok=True)

    # ---------------------------------------------------------
    # Copy shared project configuration.
    # ---------------------------------------------------------

    for template in config_templates.iterdir():
        destination = project_root / template.name

        if destination.exists():
            print(f"INFO: Preserving existing file: {destination}")
            continue

        if template.is_dir():
            shutil.copytree(template, destination)
        else:
            shutil.copy2(template, destination)

        print(f"INFO: Created: {destination}")

    # ---------------------------------------------------------
    # Determine the selected framework.
    # ---------------------------------------------------------

    frontend_config_path = project_root / "skeleton-config.json"
    dependencies_path = project_root / "skeleton-dependencies.json"

    if framework is not None:
        selected_framework = framework

    elif frontend_config_path.is_file():
        existing_config = read_json(frontend_config_path)
        selected_framework = existing_config.get("framework", "react")

        if (
            not isinstance(selected_framework, str)
            or selected_framework not in SUPPORTED_FRAMEWORKS
        ):
            raise ValueError(
                f"Invalid framework in {frontend_config_path}: "
                f"{selected_framework!r}"
            )

    else:
        selected_framework = "react"

    profile = profiles_root / selected_framework

    if not profile.is_dir():
        raise FileNotFoundError(
            f"Framework profile not found: {profile}"
        )

    profile_config_path = profile / "skeleton-config.json"
    profile_dependencies_path = profile / "skeleton-dependencies.json"

    for path in (profile_config_path, profile_dependencies_path):
        if not path.is_file():
            raise FileNotFoundError(
                f"Required framework profile file not found: {path}"
            )

    # Read and validate both profile files before writing either.
    frontend_config = read_json(profile_config_path)
    dependencies = read_json(profile_dependencies_path)

    # Ensure the selected profile identifies itself correctly.
    frontend_config["framework"] = selected_framework

    # ---------------------------------------------------------
    # Generate the root-level framework configuration.
    # ---------------------------------------------------------

    # Explicit selection resets both framework-managed files
    # to the chosen profile defaults.
    #
    # Without an explicit selection, preserve existing files
    # and create only files that are missing.

    if framework is not None or not frontend_config_path.exists():
        write_json(frontend_config_path, frontend_config)
        print(f"INFO: Created/updated: {frontend_config_path}")
    else:
        print(f"INFO: Preserving existing file: {frontend_config_path}")

    if framework is not None or not dependencies_path.exists():
        write_json(dependencies_path, dependencies)
        print(f"INFO: Created/updated: {dependencies_path}")
    else:
        print(f"INFO: Preserving existing file: {dependencies_path}")

    print(f"INFO: Selected frontend framework: {selected_framework}")
    print("INFO: Configuration complete")
