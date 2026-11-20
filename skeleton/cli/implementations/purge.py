import shutil

from typing import Any

from ...context.mode import Mode
from ...context.context import CLIContext

def purge(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True

    # for client use only!
    backend = values.get("backend", False) is True
    frontend = values.get("frontend", False) is True

    framework = context.mode == Mode.FRAMEWORK

    from ...layout.client import ClientLayout
    from ...layout.framework import FrameworkLayout

    layout: FrameworkLayout | ClientLayout

    if framework and (backend or frontend):
        raise ValueError(
            "--backend and --frontend flags"
            " "
            "are only available to client."
        )

    if framework:

        layout = context.FRAMEWORK
        root = layout.root

        targets = layout.artifacts

    else:

        layout: ClientLayout | None = context.CLIENT

        if layout is None:
            raise RuntimeError("Client layout is unavailable.")

        root = layout.root

        if not layout.backend.root.is_dir():
            print("Client backend directory not found.")
            return 1

        # No resource specified means purge both.
        if not backend and not frontend:
            backend = frontend = True

        targets = []

        if backend:
            targets.extend(layout.backend.artifacts)

        if frontend:
            targets.extend(layout.frontend.artifacts)

    removed = []

    for path in targets:

        if not path.exists() and not path.is_symlink():
            continue

        removed.append(path)

    from ...cmd.confirm import confirm

    if removed:

        print("\nThe following items will be purged:\n")

        for path in removed:
            print(f"    {path.relative_to(root)}")

        print()

        if not dry:
            if not confirm(
                "Are you sure you want to purge "
                f"{len(removed)} item(s) from: \n"
                f"{root}?"
            ):
                print("\nPurge cancelled.\n")
                return 0

    for path in removed:

        if dry:
            print(f"Will remove: {path.relative_to(root)}")

        else:
            if path.is_dir() and not path.is_symlink():
                shutil.rmtree(path)
            else:
                path.unlink()

            if verbose:
                print(f"Removed: {path.relative_to(root)}")

    if removed:
        action = "to purge" if dry else "purged"
        print(f"\n{len(removed)} item(s) {action}.")

    else:
        print("\nNothing to purge.")

    if dry:
        print("\nDRY RUN: No files or directories removed!")

    return 0