from pathlib import Path

def display(
    *,
    description: str,
    command: list[str],
    cwd: Path,
    outdir: Path | None = None,
) -> None:

    import textwrap
    WIDTH = 100
    
    command_text = " ".join(command)
    command_lines = textwrap.wrap(
        command_text,
        width=WIDTH,
        break_long_words=False,
        break_on_hyphens=False,
    )

    print(f"\n{description}")
    print(f"\n  Working directory : {cwd}")

    if outdir is not None:
        print(f"  Output directory  : {outdir}")

    print("\n  Command:")

    for line in command_lines:
        print(f"{" "*2}{line}")

    print()