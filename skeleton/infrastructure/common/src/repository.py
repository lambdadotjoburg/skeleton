from dataclasses import dataclass

# come back to this, to ensure only
# load what's needed in each layer
# store runtime/boostrap confiugration settings!
@dataclass(frozen=True, kw_only=True)
class ConfigRepository:
    servers: dict # only gateway
    schemas: dict # only gateway
    frontend: dict # only gateway
    proxy: dict # only gateway
    services: dict # only gateway