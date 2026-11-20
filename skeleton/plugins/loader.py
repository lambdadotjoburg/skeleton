import sys, importlib

from pathlib import Path

from types import ModuleType

from collections.abc import Callable

ModuleFilter = Callable[[Path], bool]

def loader(
    *,
    root: Path,
    directory: Path,
    filter: ModuleFilter | None = None,
) -> list[ModuleType]:

    root = root.resolve()
    directory = directory.resolve()

    # Make the import root available to Python.
    project = str(root)

    if project not in sys.path:
        sys.path.insert(0, project)

    # Derive the package namespace.
    package = ".".join(
        directory.relative_to(root).parts
    )

    modules: list[ModuleType] = []

    # Recursively discover Python modules.
    for path in sorted(directory.rglob("*.py")):

        if filter is not None and not filter(path):
            continue

        relative = path.relative_to(directory)

        # Ignore private directories and modules.
        if any(
            part.startswith("_") and part != "__init__.py"
            for part in relative.parts
        ):
            continue

        # Derive the module path relative to the package.
        parts = list(
            relative.with_suffix("").parts
        )

        # Handle package initializers.
        if parts[-1] == "__init__":
            parts.pop()

        suffix = ".".join(parts)

        module_name = (
            f"{package}.{suffix}"
            if suffix
            else package
        )

        module = importlib.import_module(module_name)

        modules.append(module)

    return modules