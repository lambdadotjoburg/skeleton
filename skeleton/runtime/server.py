import dataclasses

from enum import StrEnum

class ServerName(StrEnum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    GATEWAY = "gateway"

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class Server:
    host: str
    port: int
