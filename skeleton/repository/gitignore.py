# import dataclasses

# from pathlib import Path

# from pathspec import GitIgnoreSpec

# @dataclasses.dataclass(
#     kw_only=True,
#     frozen=True,
# )
# class GitIgnore:

#     root: Path

#     spec: GitIgnoreSpec | None = dataclasses.field(init=False)

#     def __post_init__(self) -> None:

#         # path = self.root / ".gitignore"
#         path = self.root / ".gitignore"

#         spec = None

#         if path.is_file():
#             with path.open("r", encoding="utf-8") as file:
#                 spec = GitIgnoreSpec.from_lines(file)

#         object.__setattr__(self, "spec", spec)

#     def load(self) -> GitIgnoreSpec | None:
#         return self.spec

#     def matches(self, path: Path) -> bool:

#         if self.spec is None:
#             return False

#         path = path.resolve()

#         relative = path.relative_to(self.root.resolve())
#         pattern = relative.as_posix()

#         if path.is_dir() and not path.is_symlink():
#             pattern += "/"

#         return self.spec.match_file(pattern)