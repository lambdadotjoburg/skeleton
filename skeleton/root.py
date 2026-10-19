import shutil

from pathlib import Path

def _remove_path(
    path: Path,
) -> None:

    if path.is_dir() and not path.is_symlink():

        shutil.rmtree(path)

        print(f"Removed directory: {path}")

    elif path.is_file() or path.is_symlink():

        path.unlink()

        print(f"Removed file: {path}")

def clean_framework(
    framework_root: Path,
) -> int:

    framework_root = framework_root.resolve()

    # Remove generated Python distribution artifacts and
    # JavaScript/TypeScript package build outputs.
    #
    # Keep node_modules, lockfiles, the development virtual
    # environment, and packaged framework tarballs intact.

    targets = [
        framework_root / "dist",
        framework_root / "skeleton_framework.egg-info",
        framework_root / ".mypy_cache",
        framework_root / "skeleton" / "packages" / "cli" / "dist",
        framework_root / "skeleton" / "packages" / "webpack" / "dist",
    ]

    for target in targets:

        _remove_path(target)

    # Remove TypeScript build information from the framework's
    # own package sources without traversing node_modules.

    package_directories = [
        framework_root / "skeleton" / "packages" / "cli",
        framework_root / "skeleton" / "packages" / "webpack",
    ]

    for directory in package_directories:

        if not directory.is_dir():
            continue

        for target in directory.glob("*.tsbuildinfo"):

            _remove_path(target)

    print("Framework clean completed.")

    return 0

def purge_framework(
    framework_root: Path,
) -> int:

    framework_root = framework_root.resolve()

    # Purge includes clean, plus installed development
    # dependencies, lockfiles, and packaged client tarballs.
    #
    # The framework's Python virtual environment is preserved.

    clean_framework(framework_root)

    targets = [
        framework_root / "node_modules",
        framework_root / "skeleton" / "packages" / "cli" / "node_modules",
        framework_root / "skeleton" / "packages" / "webpack" / "node_modules",
        framework_root / "package-lock.json",
        framework_root / "skeleton" / "packages" / "cli" / "package-lock.json",
        framework_root / "skeleton" / "packages" / "webpack" / "package-lock.json",
        framework_root / "skeleton" / "packages" / ".skeleton",
    ]

    for target in targets:

        _remove_path(target)

    print("Framework purge completed.")

    return 0

def main(
    argv: list[str] | None = None,
    framework_root: Path | None = None,
    project_root: Path | None = None,
) -> int:

    import sys

    args = sys.argv[1:] if argv is None else argv

    if framework_root is None:

        framework_root = Path(__file__).resolve().parent.parent

    framework_root = framework_root.resolve()

    if project_root is None:

        project_root = Path.cwd().resolve()

    project_root = project_root.resolve()

    from skeleton.cli import is_framework_repository

    if not is_framework_repository(framework_root):

        print(
            "Error: Framework development commands require "
            "the Skeleton framework source repository."
        )

        return 2

    if not args:

        print(
            "Usage: python run.py "
            "--bootstrap | --dist | --init | --install | "
            "--pack | --build | --clean | --purge"
        )

        return 0

    command = args[0]

    if command == "--bootstrap":

        from skeleton.infrastructure.bootstrap.src.commands.dev.init import (
            dev_init,
        )

        from skeleton.infrastructure.bootstrap.src.commands.dev.install import (
            dev_install,
        )

        print("\n[1/2] Initializing framework development...\n")

        dev_init(framework_root)

        print("\n[2/2] Installing framework development dependencies...\n")

        dev_install(framework_root)

        print("\nFramework bootstrap completed successfully.")

        return 0

    if command == "--dist":

        from skeleton.infrastructure.bootstrap.src.commands.dev.pack import (
            dev_pack,
        )

        from skeleton.infrastructure.bootstrap.src.commands.dev.build import (
            dev_build,
        )

        print("\n[1/2] Packaging framework dependencies...\n")

        dev_pack(framework_root)

        print("\n[2/2] Building framework distribution...\n")

        dev_build(framework_root)

        print("\nFramework distribution completed successfully.")

        return 0

    if command == "--init":

        from skeleton.infrastructure.bootstrap.src.commands.dev.init import (
            dev_init,
        )

        dev_init(framework_root)

        return 0

    if command == "--install":

        from skeleton.infrastructure.bootstrap.src.commands.dev.install import (
            dev_install,
        )

        dev_install(framework_root)

        return 0

    if command == "--pack":

        from skeleton.infrastructure.bootstrap.src.commands.dev.pack import (
            dev_pack,
        )

        dev_pack(framework_root)

        return 0

    if command == "--build":

        from skeleton.infrastructure.bootstrap.src.commands.dev.build import (
            dev_build,
        )

        dev_build(framework_root)

        return 0

    if command == "--clean":

        return clean_framework(framework_root)

    if command == "--purge":

        return purge_framework(framework_root)

    raise ValueError(f"Unknown framework command: {command}")