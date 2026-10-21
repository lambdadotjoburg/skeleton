import sys

from pathlib import Path

# ============================================================
# Framework commands (run from the framework root)
# ============================================================

# python run.py --bootstrap
# python run.py --dist

# python run.py --init
# python run.py --install
# python run.py --pack
# python run.py --build

# python run.py --clean
# python run.py --purge

# python path/to/run.py --config
# python path/to/run.py --init
# python path/to/run.py --install
# python path/to/run.py --start frontend gateway packages --open

# ============================================================
# Client commands (run from a client project root)
# ============================================================

# skeleton --config
# skeleton --config react
# skeleton --config solid
# skeleton --config vue

# skeleton --init
# skeleton --install
# skeleton --start
# skeleton --start frontend gateway --open

# skeleton --quickstart

# skeleton --serve
# skeleton --build
# skeleton --preview
# skeleton --clean
# skeleton --purge

def is_framework_repository(
    path: Path,
) -> bool:

    path = path.resolve()

    return (
        (path / "run.py").is_file()
        and (path / "pyproject.toml").is_file()
        and (path / "skeleton" / "infrastructure").is_dir()
        and (path / "skeleton" / "packages").is_dir()
    )

def main(
    argv: list[str] | None = None,
    framework_root: Path | None = None,
) -> int:

    args = sys.argv[1:] if argv is None else argv

    # When installed through PyPI, skeleton/cli.py lives inside
    # site-packages/skeleton/. Its parent directory is site-packages.
    #
    # In the source repository,
    # its parent directory is the
    # framework repository root.

    if framework_root is None:

        framework_root = Path(__file__).resolve().parent.parent

    framework_root = framework_root.resolve()
    project_root = Path.cwd().resolve()

    # Framework commands and client commands share some names.
    #
    # When running from the actual framework source repository,
    # dispatch to root.py.
    #
    # Otherwise, dispatch client commands to client.py.

    is_framework_root = is_framework_repository(project_root)

    if not args:

        print(
            "Usage: skeleton "
            "--config | --init | --install | --start | --quickstart"
        )

        return 0

    command = args[0]

    # These commands only operate on the framework source repository.
    # Route them to root.py regardless of the current directory so
    # root.py can report a clear error if necessary.

    root_only_commands = {
        "--bootstrap",
        "--dist",
        "--pack",
    }

    # Shared command names are interpreted according to the
    # current working directory.

    root_or_client_commands = {
        "--init",
        "--install",
        "--build",
        "--clean",
        "--purge",
    }

    if command in root_only_commands:

        from skeleton.root import main as root_main

        return root_main(
            argv=args,
            framework_root=(
                project_root
                if is_framework_root
                else framework_root
            ),
            project_root=project_root,
        )

    if command in root_or_client_commands and is_framework_root:

        from skeleton.root import main as root_main

        return root_main(
            argv=args,
            framework_root=project_root,
            project_root=project_root,
        )

    from skeleton.client import main as client_main

    return client_main(
        argv=args,
        framework_root=framework_root,
        project_root=project_root,
    )


if __name__ == "__main__":
    raise SystemExit(main())