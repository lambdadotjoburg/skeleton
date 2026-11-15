from typing import Any

from ..layout.client import ClientLayout

from ..context.mode import Mode
from ..context.context import CLIContext

from ..versioning.read import read_pyproject_version
from ..versioning.read import read_package_version

from ..versioning.resolve import resolve_version

from ..versioning.write import write_pyproject_version
from ..versioning.write import write_package_version

def bump_framework(
    *, 
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True

    force = values.get("froce", False) is True

    pyproject = context.FRAMEWORK.pyproject

    py_version = read_pyproject_version(pyproject)

    if py_version is None:
        return 1

    framework_version = resolve_version(
        py_version,
        major=values["major"],
        minor=values["minor"],
        patch=values["patch"],
    )

    print(
        f"{'.'.join(map(str, py_version))}"
        f" -> "
        f"{'.'.join(map(str, framework_version))}"
    )

    if dry:
        print("DRY RUN: No files modified!")
        return 0

    if not force:

        from ..cmd.confirm import confirm

        if not confirm("Confirm version update?"):
            print("Version update cancelled!")
            return 0

    if verbose:
        print(f"Updating: {pyproject}")

    if not write_pyproject_version(
        pyproject,
        framework_version,
    ):
        return 1

    print("Version:", framework_version)

    return 0

def bump_client(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True

    backend = values.get("backend", False) is True
    frontend = values.get("frontend", False) is True

    sync = values.get("sync", False) is True
    force = values.get("force", False) is True

    if sync or (not backend and not frontend):
        backend = True
        frontend = True

    client = ClientLayout(root=context.cwd)

    py_version = None
    package_version = None

    # Read existing versions

    if backend:

        py_version = read_pyproject_version(
            client.backend.pyproject
        )

        if py_version is None:
            return 1

    if frontend:

        package_version = read_package_version(
            client.frontend.package
        )

        if package_version is None:
            return 1

    # Resolve new versions

    if sync:

        assert py_version is not None
        assert package_version is not None

        current_version = max(py_version, package_version)

        synced_version = resolve_version(
            current_version,
            major=values["major"],
            minor=values["minor"],
            patch=values["patch"],
        )

        backend_version = synced_version
        frontend_version = synced_version

    else:

        if backend:

            assert py_version is not None

            backend_version = resolve_version(
                py_version,
                major=values["major"],
                minor=values["minor"],
                patch=values["patch"],
            )

        if frontend:

            assert package_version is not None

            frontend_version = resolve_version(
                package_version,
                major=values["major"],
                minor=values["minor"],
                patch=values["patch"],
            )

    if backend:

        assert py_version is not None

        print(
            "Backend: "
            f"{'.'.join(map(str, py_version))}"
            " -> "
            f"{'.'.join(map(str, backend_version))}"
        )

    if frontend:

        assert package_version is not None

        print(
            "Frontend: "
            f"{'.'.join(map(str, package_version))}"
            " -> "
            f" -> {'.'.join(map(str, frontend_version))}"
        )

    if dry:
        print("DRY RUN: no files modified!")
        return 0

    if not force:

        from ..cmd.confirm import confirm

        if not confirm("Confirm version update?"):

            print("Version update cancelled!")
            
            return 0

    # Write resolved versions

    if backend:

        if verbose:
            print(f"Updating: {client.backend.pyproject}")

        if not write_pyproject_version(
            client.backend.pyproject,
            backend_version,
        ):
            return 1

        print("Backend:", backend_version)

    if frontend:

        if verbose:
            print(f"Updating: {client.frontend.package}")

        if not write_package_version(
            client.frontend.package,
            frontend_version,
        ):
            return 1

        print("Frontend:", frontend_version)

    return 0

def bump(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    if context.mode == Mode.FRAMEWORK:
        return bump_framework(
            values=values,
            context=context,
        )

    return bump_client(
        values=values,
        context=context,
    )