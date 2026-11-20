from typing import Any

from pathlib import Path

from ...context.context import CLIContext

def readme(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    write = values.get("write")
    section = values.get("section")

    docs = context.FRAMEWORK.DOCUMENTATION
    
    content = docs.readme(section=section)

    if write is not None:

        path = Path(write).expanduser()

        if not path.is_absolute():
            path = context.cwd / path

        if path.exists():

            existing = path.read_text(encoding="utf-8")

            if existing == content:
                print(f"{path} is already up to date.")
                return 0

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            content,
            encoding="utf-8",
        )

        print(f"Generated: {path}")
        return 0

    print(content)

    return 0