from typing import Any

class ReloadConfig:

    def __init__(self, data: dict[str, Any]):

        self.enabled: bool = data.get("enabled", True) is True
        self.directories: list[str] =data.get("directories", [])
        self.extensions: list[str] =data.get("extensions", [])
