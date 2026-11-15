from pathlib import Path

from skeleton import cli

if __name__ == "__main__":
    raise SystemExit(
        cli(
            root=Path(
                __file__
            ).resolve().parent,
        )
    )