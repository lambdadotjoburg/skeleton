import json

from typing import Any

from ..context.context import CLIContext

def merge_settings(
    defaults: dict[str, Any],
    existing: dict[str, Any],
) -> dict[str, Any]:

    settings = defaults.copy()

    for key, value in existing.items():

        if (
            isinstance(value, dict)
            and isinstance(settings.get(key), dict)
        ):

            settings[key] = merge_settings(
                settings[key],
                value,
            )

        else:

            settings[key] = value

    return settings

def vscode(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True

    feature = values["feature"]

    from ..context.mode import Mode
    from ..layout.client import ClientLayout
    from ..layout.framework import FrameworkLayout

    layout: FrameworkLayout | ClientLayout

    if context.mode == Mode.FRAMEWORK:

        layout = context.FRAMEWORK

        source = layout.BOILERPLATE.vscode.config.path(
            "framework/settings.json"
        )

        variables = {

            "venv": layout.venv.relative_to(
                layout.root
            ).as_posix(),

            "venv_python": layout.venv_python.relative_to(
                layout.root
            ).as_posix(),
        }

        description = "Generating Skeleton's vscode settings ..."

    else:

        layout = ClientLayout(root=context.cwd)

        source = context.FRAMEWORK.BOILERPLATE.vscode.config.path(
            "app/settings.json"
        )

        variables = {
            
            "backend": layout.backend.dir,

            "venv": layout.backend.venv.relative_to(
                layout.backend.root
            ).as_posix(),

            "venv_python": layout.backend.venv_python.relative_to(
                layout.backend.root
            ).as_posix(),
        }

        description = "Generating vscode settings ..."

    from ..template.render import render

    templates = json.loads(
        render(
            source.read_text(encoding="utf-8"),
            variables=variables,
        )
    )

    settings = templates[feature]

    destination = layout.vscode

    if destination.exists():

        existing = json.loads(
            destination.read_text(encoding="utf-8")
        )

    else:

        existing = {}

    settings = merge_settings(settings, existing)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    destination.write_text(
        json.dumps(settings, indent=4) + "\n",
        encoding="utf-8",
    )

    if verbose:

        print(description)
        print(f"Settings written to: {destination}")

    return 0