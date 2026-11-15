import shutil

from datetime import datetime

from typing import Any, TypeAlias

from ..decorators.roles import roles

from ..context.roles import Role
from ..context.context import CLIContext

Report: TypeAlias = list[tuple[str, str]]

def display(values: dict[str, Any]) -> None:

    print("\nProject configuration:\n")

    for name, value in values.items():
        print(f"\t{name}: {value}")

def generate(
    *,
    values: dict[str, Any],
    context: CLIContext,
    dry: bool = False,
) -> Report | None:

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    boilerplate = context.FRAMEWORK.BOILERPLATE

    profile = boilerplate.profile(
        values.get("profile", "vanilla")
    )

    source = boilerplate.config.paths(
        "skeleton-*.json",
        exclude="skeleton-metadata.json"
    )

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    try:
        profile.config.require("skeleton-dependencies.json")

        source.append(
            profile.config.path(
                "skeleton-dependencies.json"
            )
        )

        boilerplate.config.require(
            [
                "skeleton-fastapi.json",
                "skeleton-metadata.json",
                "skeleton-portal.json",
                "skeleton-project.json",
                "skeleton-proxy.json",
                "skeleton-schemas.json",
                "skeleton-servers.json",
            ]
        )

    except FileNotFoundError as error:

        print(error)
        return None

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    from ..layout.client import ClientLayout

    layout = ClientLayout(root=context.cwd)

    dest = layout.config.root

    if not dry:
        dest.mkdir(parents=True, exist_ok=True)

    report: list[tuple[str, str]] = []

    for file in source:

        target = dest / file.name

        if target.exists():

            report.append(("-", target.name))

            continue

        if not dry:
            shutil.copy2(file, target)

        report.append(("+", target.name))

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    # create template variables!

    variables = {
        "date": datetime.now().date().isoformat(),
        "profile": profile.name,
        "name": values["name"],
        "title": values["title"],
        "version": values["version"],
        "author": values["author"],
        "description": values["description"],
        "license": values["license"],
    }

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    # render template variables!

    from ..template.render import render

    metadata = render(
        boilerplate.config.path(
            "skeleton-metadata.json"
        ).read_text(encoding="utf-8"),
        variables=variables
    )

    target = dest / "skeleton-metadata.json"

    if target.exists():

        report.append(("-", target.name))

    else:

        if not dry:

            target.write_text(
                metadata,
                encoding="utf-8",
            )

        report.append(("+", target.name))

    return report

def collect(
    *, 
    values: dict[str, Any],
    context: CLIContext
) -> None:

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#
    
    command = context.REGISTRY.get("config")

    assert command is not None

    arguments = command.definition.arguments

    print(
        "\n" +
        "Configure project:" +
        "\n"
    )

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    # prompt user for metadata input!

    from ..cmd.prompt import prompt

    for name, value in values.items():

        allowed = arguments.get(name)

        choices = (
            allowed
            if isinstance(allowed, list)
            else None
        )

        values[name] = prompt(
            name,
            str(value),
            choices=choices,
        )

@roles(Role.CLIENT)
def config(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    command = context.REGISTRY.get("config")

    if command is None:
        raise RuntimeError("Config command not registered.")
    
    verbose = values.pop("verbose", False) is True
    dry = values.pop("dry", False) is True

    display(values)

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    from ..cmd.confirm import confirm

    if not confirm(
        message=("Accept default config?")
    ):
        collect(
            values=values,
            context=context,
        )

    # validate the client's supplied cli input!

    from ..validation.validate import validate
    from ..validation.metadata import METADATA_RULES

    errors = validate(
        values=values,
        rules=METADATA_RULES,
    )

    if errors:
        for error in errors:
            print(error)
        return 1

    # if errors, handle ...

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    # handle display/verbose/dry/report!
    
    if verbose:
        display(values)

    report = generate(
        values=values,
        context=context,
        dry=dry,
    )

    if report is None:
        return 1

    created = [
        name
        for status, name in report
        if status == "+"
    ]

    if verbose:

        if created:

            heading = (
                "Config files to create:"
                if dry
                else "Config files created:"
            )

            print(f"\n{heading}\n")

            for name in created:
                print(f"  + {name}")

        else:
            print("\nConfiguration already up to date!")

    if dry:
        print("\nDRY RUN: No config files modified!")

    return 0

    #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#
