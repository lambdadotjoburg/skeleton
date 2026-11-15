import shutil

from pathlib import Path

from .plan import ProjectPlan

def generate(
    plan: ProjectPlan,
    *,
    verbose: bool = False,
    dry: bool = False
):
    display = verbose or dry

    # create client's folder/directory structure
    root_exists = plan.root.exists()

    if display:
        action = "Merging directory" if root_exists else "Creating directory"
        if dry:
            action = "Will merge directory" if root_exists else "Will create directory"
        print(f"{action}: {plan.root}")

    if not dry:
        plan.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    # Identify all template source files.
    templates_src = {
        template.source.resolve()
        for template in plan.templates
    }

    # Merge-copy boilerplate directories.
    for source, destination in plan.folders:

        if not source.is_dir():
            raise NotADirectoryError(
                f"Boilerplate directory not found: {source}"
            )

        exists = destination.exists()

        if display:
            action = "Merging directory" if exists else "Creating directory"
            if dry:
                action = "Will merge directory" if exists else "Will create directory"
            print(f"{action}: {destination}")

        if dry:
            continue

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        def copy_file(source: str, destination: str) -> str:
            if Path(destination).exists():
                return destination

            return shutil.copy2(source, destination)

        def ignore(directory: str, names: list[str]) -> set[str]:

            path = Path(directory)

            return {
                name
                for name in names
                if (path / name).resolve()
                    in templates_src
            }

        shutil.copytree(
            source,
            destination,
            dirs_exist_ok=True,
            ignore=ignore,
            copy_function=copy_file
        )

    # Copy individual boilerplate files.
    for source, destination in plan.files:

        if not source.is_file():
            raise FileNotFoundError(
                f"Boilerplate file not found: {source}"
            )

        exists = destination.exists()

        if display:
            if dry:
                action = "Will skip existing file" if exists else "Will create file"
            else:
                action = "Skipping existing file" if exists else "Creating file"
            print(f"{action}: {destination}")

        if exists:
            continue

        if not dry:
            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(source, destination)

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    # Write templates after copying!
    
    for template in plan.templates:

        destination = template.destination

        if destination.exists():

            if not destination.is_file():
                raise IsADirectoryError(
                    "Expected a file but "
                    "found a directory: "
                    f"{destination}"
                )

            if display:
                action = (
                    "Will skip existing template"
                    if dry
                    else "Skipping existing template"
                )
                print(f"{action}: {destination}")

            continue

        if display:
            action = (
                "Will create template"
                if dry
                else "Creating template"
            )
            print(f"{action}: {destination}")

        if not dry:

            destination.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if isinstance(template.content, bytes):
                destination.write_bytes(template.content)

            else:

                assert template.content is not None

                destination.write_text(
                    template.content,
                    encoding="utf-8",
                )