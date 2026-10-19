from pathlib import Path

from skeleton.cli import main

if __name__ == "__main__":

    raise SystemExit(
        
        main(
            framework_root=Path(__file__).resolve().parent,
        )
    )