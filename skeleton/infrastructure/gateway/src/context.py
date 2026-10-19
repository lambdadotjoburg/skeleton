from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ProcessContext:
    module: str
    exe: Path
    cwd: Path

@dataclass(frozen=True, kw_only=True)
class NetworkContext:
    host: str
    port: int

@dataclass(frozen=True, kw_only=True)
class WatchContext:
    enabled: bool
    directory: Path
    extensions: tuple[str, ...]

@dataclass(frozen=True, kw_only=True)
class ServiceContext:

    id: str # backend (ALWAYS!) [FOR NOW!]
    name: str # app => actual FastAPI app name
    root: Path # resolving module paths, file paths, etc.

    network: NetworkContext
    process: ProcessContext
    watch: WatchContext
    