from pathlib import Path

from skeleton.infrastructure.common.src.loader import load
from skeleton.infrastructure.common.src.repository import ConfigRepository

def load_runtime_config(
    path: Path,
    project_root: Path,
    framework_root: Path,
    # layout: ProjectLayout,
) -> ConfigRepository:

    CONFIG = load(path)["config"]

    data: dict = {}

    for name, config in CONFIG.items():

        root = (
            project_root
            if name in ("servers", "schemas")
            else framework_root
        )

        data[name] = load(root / config)

    # frontend_config = layout.frontend / "skeleton-config.json"
    frontend_config = project_root / "skeleton-config.json"
    data["frontend"] = load(frontend_config)

    return ConfigRepository(
        servers=data["servers"],
        schemas=data["schemas"],
        frontend=data["frontend"],
        proxy=data["proxy"],
        services=data["services"],
    )