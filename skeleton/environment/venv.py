from pathlib import Path

def create_venv(
    *,
    target: Path,
) -> Path:

    import venv

    venv.EnvBuilder(
        with_pip=True,
    ).create(target)

    return target