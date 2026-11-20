from pathlib import Path

from ..repository.manifest import PyProjectManifest

from ..environment.resolver import resolve_interpreter

from ..environment.resolver import Resolver

class PythonLayout:

    root: Path
    
    resolver: Resolver = staticmethod(resolve_interpreter)

    @property
    def main(self) -> Path:
        return  self.root / "main.py"

    @property
    def module(self) -> str:
        return self.main.stem

    @property
    def venv(self) -> Path:
        return self.root / ".venv"

    @property
    def venv_python(self) -> Path:
        return self.resolver(self.venv)

    @property
    def pyproject(self) -> Path:
        return self.root / "pyproject.toml"

    @property
    def manifest(self) -> PyProjectManifest:
        return PyProjectManifest(path=self.pyproject)
    
    # @property
    # def mypy_cache(self) -> list[Path]:
    #     return list(self.root.rglob(".mypy_cache"))
