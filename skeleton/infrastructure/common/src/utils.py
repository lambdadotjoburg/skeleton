import os
from pathlib import Path

def resolve_executable_path(path) -> Path:
    if os.name == "nt":
        return Path(path)/".venv"/"Scripts"/"python.exe"
    else:
        return Path(path)/".venv"/"bin"/"python"
    
def check_file_exists(filename: str, path: Path):

    if not path.exists():
        raise FileNotFoundError(
            f"{filename}: file does not exist {path}"
        )
    
    if not path.is_file():
        raise IsADirectoryError(
            f"{filename}: path is not a file {path}"
        )

def module_to_path(module: str) -> Path:
    return Path(module.replace(".", "/")).with_suffix(".py")

def path_to_module(path: Path) -> str:
    return ".".join(path.with_suffix("").parts)
