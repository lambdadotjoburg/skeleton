import ast

from pathlib import Path

from collections.abc import Callable

def decorated(
    name: str,
) -> Callable[[Path], bool]:
    
    def predicate(path: Path) -> bool:

        source = path.read_text(encoding="utf-8")

        tree = ast.parse(source)

        for node in ast.walk(tree):

            if not isinstance(
                node, (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                continue

            for decorator in node.decorator_list:

                if isinstance(decorator, ast.Call):
                    decorator = decorator.func

                if isinstance(decorator, ast.Name):
                    if decorator.id == name:
                        return True

                if isinstance(decorator, ast.Attribute):
                    if decorator.attr == name:
                        return True

        return False

    return predicate