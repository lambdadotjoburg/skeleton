from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class ProcessConfig:
    module: str

@dataclass(frozen=True, kw_only=True)
class NetworkConfig:
    host: str
    port: int

@dataclass(frozen=True, kw_only=True)
class WatchConfig:
    enabled: bool
    extensions: tuple[str, ...]

@dataclass(frozen=True, kw_only=True)
class ServiceConfig:

    id: str # backend (ALWAYS!) [FOR NOW!]
    name: str # app => actual FastAPI app name
    root: Path # resolving module paths, file paths, etc.

    # service specs
    network: NetworkConfig
    process: ProcessConfig
    watch: WatchConfig
    