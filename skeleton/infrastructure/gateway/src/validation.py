from pathlib import Path

from skeleton.infrastructure.gateway.src.config import ServiceConfig
from skeleton.infrastructure.gateway.src.context import ServiceContext

from skeleton.infrastructure.common.src.utils import (
    check_file_exists,
    module_to_path,
)

class ConfigValidationError(Exception):
    pass

def validate_service_configs(
    services: list[ServiceConfig],
) -> bool:

    used_ports: set[int] = set()

    for service in services:
        validate_service_root(service.root)

        validate_service_module(
            service.process.module,
            service.root,
        )

        validate_service_port(
            service.network.port,
            used_ports,
        )

    return True


def validate_service_contexts(
    services: list[ServiceContext],
) -> bool:

    for service in services:
        validate_service_executable(service.process.exe)
        validate_service_watch_dir(service.watch.directory)
        validate_service_cwd(service.process.cwd)

    return True

def validate_service_root(root: Path) -> None:
    if not root.exists():
        raise FileNotFoundError(
            f"service root does not exist: {root}"
        )


def validate_service_module(
    module: str,
    root: Path,
) -> None:

    path = root / module_to_path(module)
    
    check_file_exists("module", path)


def validate_service_port(
    port: int,
    used_ports: set[int],
) -> None:

    if port in used_ports:
        raise ConfigValidationError(
            f"Duplicate port detected: {port}"
        )

    used_ports.add(port)

def validate_service_executable(exe: Path) -> None:
    check_file_exists("exe", exe)

def validate_service_cwd(cwd: Path) -> None:
    if not cwd.exists():
        raise FileNotFoundError(
            f"cwd does not exist: {cwd}"
        )

def validate_service_watch_dir(watch_dir: Path) -> None:
    if not watch_dir.exists():
        raise FileNotFoundError(
            f"watch directory does not exist: {watch_dir}"
        )