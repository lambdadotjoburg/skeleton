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

def copy_app_template(
    source: Path,
    target: Path,
    frontend: str,
    backend: str,
) -> None:

    target.mkdir(parents=True, exist_ok=True)

    directories = {
        "frontend": frontend,
        "backend": backend,
    }

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