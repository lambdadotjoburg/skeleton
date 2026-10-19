import shutil

from pathlib import Path

def config(
    framework_root: Path,
    project_root: Path,
) -> None:

    templates = (
        framework_root
        / "skeleton"
        / "infrastructure"
        / "bootstrap"
        / "src"
        / "templates"
        / "config"
    )

    if not templates.is_dir():
        
        raise FileNotFoundError(
            f"Configuration templates not found: {templates}"
        )

    project_root = project_root.resolve()

    project_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    for template in templates.iterdir():

        destination = project_root / template.name

        if destination.exists():

            print(
                f"INFO: Preserving existing file: {destination}"
            )
            continue

        if template.is_dir():

            shutil.copytree(template, destination)

        else:

            shutil.copy2(template, destination)

        print(f"INFO: Created: {destination}")

    print("INFO: Configuration complete")
