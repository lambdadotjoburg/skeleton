from typing import Any

from ...decorators.roles import roles
from ...context.roles import Role
from ...context.context import CLIContext

def report(
    *,
    resource: str,
    path: str,
    changes: dict[str, dict[str, dict[str, str]]],
) -> None:

    print(f"\n{resource.capitalize()} dependencies:")
    print(f"Manifest: {path}")

    for section in ("dependencies", "devDependencies"):

        added = changes["added"][section]
        updated = changes["updated"][section]
        removed = changes["removed"][section]

        if not added and not updated and not removed:
            continue

        print(
            "\n"
            f"\t {section}:"
            "\n"
        )

        for name, version in added.items():
            print(f"\t + {name}: {version}")

        for name, version in updated.items():
            print(f"\t ~ {name}: {version}")

        for name, version in removed.items():
            print(f"\t - {name}: {version}")

@roles(Role.CLIENT)
def sync(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    layout = context.CLIENT

    if layout is None:
        raise RuntimeError("Client layout is unavailable.")

    dry = values.get("dry", False) is True
    force = values.get("force", False) is True

    backend = values.get("backend", False) is True
    frontend = values.get("frontend", False) is True

    if not backend and not frontend:
        backend = True
        frontend = True

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    try:

        if frontend:
            package = layout.frontend.package

            if not package.is_file():
                raise FileNotFoundError(package)

        if backend:
            pyproject = layout.backend.pyproject

            if not pyproject.is_file():
                raise FileNotFoundError(pyproject)

        layout.config.require("skeleton-dependencies.json")

    except FileNotFoundError as error:
        print(error)
        return 1

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    from ...repository.manifest import Manifest
    from ...repository.reconcile import reconcile

    dependencies = layout.dependencies

    manifests: dict[str, Manifest] = {}

    if frontend:
        manifests["frontend"] = layout.frontend.manifest

    if backend:
        manifests["backend"] = layout.backend.manifest

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    changes = {}

    for resource, manifest in manifests.items():

        updated = reconcile(
            existing=manifest.dependencies,
            configured=dependencies[resource],
            remove=True,
        )

        calculated = manifest.calculate(updated)

        if any(
            calculated[action][section]
            for action in ("added", "updated", "removed")
            for section in ("dependencies", "devDependencies")
        ):
            changes[resource] = (
                manifest,
                updated,
                calculated,
            )

    if not changes:
        print("manifests already in sync!")
        return 0

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    for resource, (manifest, updated, calculated) in changes.items():

        report(
            resource=resource,
            path=str(manifest.path),
            changes=calculated,
        )

    if dry:
        print("\nDRY RUN: No manifests modified!")
        return 0

    # %*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    if not force:

        from ...cmd.confirm import confirm

        if not confirm("Apply the proposed manifest changes?"):
            print("sync cancelled!")
            return 1

    # Apply and persist the already-calculated changes.
    for manifest, updated, calculated in changes.values():

        manifest.update(updated)

        manifest.path.write_text(
            manifest.dumps(),
            encoding="utf-8",
        )

    print("\nManifests synchronized successfully!")

    return 0