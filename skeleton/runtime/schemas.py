import dataclasses

from typing import Any

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class RouteSchema:
    prefix: str
    strip: bool

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class HTTPSchemas:
    backend: RouteSchema
    frontend: RouteSchema

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class WebSocketSchemas:
    backend: RouteSchema

class Schemas:

    def __init__(self, data: dict[str, Any]):

        self.http = HTTPSchemas(

            backend=RouteSchema(
                **data["http"]["backend"],
            ),

            frontend=RouteSchema(
                **data["http"]["frontend"],
            ),
        )

        self.ws = WebSocketSchemas(
            
            backend=RouteSchema(
                **data["ws"]["backend"],
            ),
        )