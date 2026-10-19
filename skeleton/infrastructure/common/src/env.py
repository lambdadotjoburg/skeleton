import os
from pathlib import Path

def build_env(ROOT: Path, MODE: str):
    base_env = os.environ.copy()
    runtime_env = {
        "APP_MODE": MODE,
        "APP_ROOT": str(ROOT),
        "PYTHONPATH": str(ROOT),
    }
    env = base_env | runtime_env
    return env