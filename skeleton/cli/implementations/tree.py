from typing import Any

from pathlib import Path

from ...context.context import CLIContext

def patterns(value: Any) -> list[str]:
    
    if value is None:
        return []
    
    if isinstance(value, str):
        return [value]
    
    if isinstance(value, (list, tuple)):
        return [
            str(pattern)
            for pattern in value
            if str(pattern).strip()
        ]
    
    return []

def tree(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    # ensure lazy import!
    from pathspec import PathSpec

    # lazily defined function!
    def matches(
        spec: PathSpec,
        path: Path,
        *,
        directory: bool = False,
    ) -> bool:
        value = path.as_posix()

        if spec.match_file(value):
            return True

        return directory and spec.match_file(f"{value}/")

    root = Path(
        values.get("dir") or "."
    ).expanduser().resolve()

    if not root.exists():
        print(f"Directory not found: {root}")
        return 1

    if not root.is_dir():
        print(f"Not a directory: {root}")
        return 1

    # Options
    dirs_only = values.get("dirs", False) is True
    files_only = values.get("files", False) is True
    
    show_hidden = (
        values.get("hidden", False) is True
        or values.get("all", False) is True
    )
    show_ignored = (
        values.get("ignored", False) is True
        or values.get("all", False) is True
    )

    show_dirs = not files_only or dirs_only
    show_files = not dirs_only or files_only

    # Maximum traversal depth
    depth_value = values.get("depth")

    try:
        max_depth = (
            int(depth_value)
            if depth_value is not None
            else None
        )
    except (TypeError, ValueError):
        print(f"Invalid depth: {depth_value!r}")
        return 1

    if max_depth is not None and max_depth < 0:
        print("Depth cannot be negative.")
        return 1

    if max_depth == 0:
        max_depth = None

    # Explicit exclusion patterns
    exclude_patterns = patterns(
        values.get("exclude")
    )

    exclude_spec = PathSpec.from_lines(
        "gitwildmatch",
        exclude_patterns,
    )

    # Root .gitignore patterns
    gitignore_spec = PathSpec.from_lines(
        "gitwildmatch", []
    )

    gitignore = root / ".gitignore"

    if not show_ignored and gitignore.is_file():
        try:
            gitignore_spec = PathSpec.from_lines(
                "gitwildmatch",
                gitignore.read_text(
                    encoding="utf-8"
                ).splitlines(),
            )
        except OSError as error:
            print(f"Could not read .gitignore: {error}")
            return 1

    # Display
    print(root.name or str(root))

    directories = 0
    files = 0

    def traverse(
        directory: Path,
        relative: Path,
        prefix: str,
        depth: int,
    ) -> None:

        nonlocal directories, files

        if max_depth is not None and depth >= max_depth:
            return

        try:
            entries = sorted(
                directory.iterdir(),
                key=lambda path: (
                    not path.is_dir(),
                    path.name.casefold(),
                ),
            )
        except PermissionError:
            return

        visible: list[tuple[Path, bool]] = []

        for path in entries:

            is_directory = path.is_dir()
            name = path.name

            # Hidden paths
            if not show_hidden and name.startswith("."):
                continue

            relative_path = relative / name

            # Explicit exclusions
            if matches(
                exclude_spec,
                relative_path,
                directory=is_directory,
            ):
                continue

            # Git-ignored paths
            if not show_ignored and matches(
                gitignore_spec,
                relative_path,
                directory=is_directory,
            ):
                continue

            # Display filters
            if is_directory and not show_dirs:
                continue

            if not is_directory and not show_files:
                continue

            visible.append((path, is_directory))

        # Files-only mode still traverses directories,
        # but displays matching files as relative paths.
        if files_only and not dirs_only:

            for path in entries:

                # Only traverse directories.
                if not path.is_dir():
                    continue

                # Do not follow symlinked directories.
                if path.is_symlink():
                    continue

                name = path.name

                if not show_hidden and name.startswith("."):
                    continue

                relative_path = relative / name

                if matches(
                    exclude_spec,
                    relative_path,
                    directory=True,
                ):
                    continue

                if not show_ignored and matches(
                    gitignore_spec,
                    relative_path,
                    directory=True,
                ):
                    continue

                traverse(
                    path,
                    relative_path,
                    prefix,
                    depth + 1,
                )

            for path, _ in visible:

                files += 1

                print(
                    f"{prefix}├── "
                    f"{(relative / path.name).as_posix()}"
                )

            return

        for index, (path, is_directory) in enumerate(visible):

            last = index == len(visible) - 1

            connector = "└── " if last else "├── "
            child_prefix = (
                prefix + (" " * 4 if last else "│" + " " * 3)
            )

            print(f"{prefix}{connector}{path.name}")

            if is_directory:
                directories += 1

                # Do not follow symlinked directories.
                if path.is_symlink():
                    continue

                traverse(
                    path,
                    relative / path.name,
                    child_prefix,
                    depth + 1,
                )
            else:
                files += 1

    traverse(
        root,
        Path(),
        "",
        0,
    )

    print(
        f"\n{directories} director"
        f"{'y' if directories == 1 else 'ies'}, "
        f"{files} file"
        f"{'s' if files != 1 else ''}"
    )

    return 0
