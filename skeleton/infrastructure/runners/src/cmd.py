from dataclasses import dataclass

@dataclass(frozen=True, kw_only=True)
class CMD:
    action: str
    targets: list[str]
    options: dict[str, str | bool]