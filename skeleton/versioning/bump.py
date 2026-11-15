# def bump_version(
#     *,
#     values: dict[str, str | bool],
#     projects: list[PythonProtocol]
# ) -> int:

#     from .read import read_version
#     from .check import check_versions
#     from .format import format_version
#     from .increment import increment_version

#     dry = values.get("dry", False) is True
#     verbose = values.get("verbose", False) is True

#     major = values.get("major", False) is True
#     minor = values.get("minor", False) is True
#     patch = values.get("patch", False) is True

#     if sum((major, minor, patch)) != 1:
#         print(
#             "Must specify exactly one version component: "
#             "--major, --minor, or --patch."
#         )
#         return 1

#     if not projects:
#         print("No Python projects supplied for versioning.")
#         return 1

#     versions: list[tuple[PythonProtocol, tuple[int, int, int]]] = []

#     for project in projects:

#         version = read_version(project=project)

#         if version is None:
#             return 1

#         versions.append((project, version))

#     current_version = check_versions(versions=versions)

#     if current_version is None:
#         return 1

#     proposed_version = increment_version(
#         current=current_version,
#         major=major,
#         minor=minor,
#         patch=patch,
#     )

#     current = format_version(current_version)
#     proposed = format_version(proposed_version)

#     # commit_version(projects, next_version)

#     if verbose:
#         print(f"Current version:  {current}")
#         print(f"Proposed version: {proposed}")

#     else:
#         print(proposed)

#     if dry:
#         print("Dry run: no changes were made.")

#     return 0