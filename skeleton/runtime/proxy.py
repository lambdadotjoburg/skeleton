import dataclasses

from typing import Any

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class ProxySettings:
    default_timeout: float
    follow_redirects: bool

@dataclasses.dataclass(
    frozen=True,
    kw_only=True,
)
class CORS:

    allow_origins: list[str]

    allow_credentials: bool

    allow_methods: list[str]
    allow_headers: list[str]

    expose_headers: list[str]

    allow_origin_regex: str | None
    allow_private_network: bool

    max_age: int

class Proxy:

    def __init__(self, data: dict[str, Any]):

        self.methods=data["methods"]

        self.settings = ProxySettings(
            default_timeout=data["settings"]["defaultTimeout"],
            follow_redirects=data["settings"]["followRedirects"],
        )

        self.cors = CORS(
            allow_origins=data["cors"]["allowOrigins"],
            allow_credentials=data["cors"]["allowCredentials"],
            allow_methods=data["cors"]["allowMethods"],
            allow_headers=data["cors"]["allowHeaders"],
            expose_headers=data["cors"]["exposeHeaders"],
            allow_origin_regex=data["cors"]["allowOriginRegex"],
            allow_private_network=data["cors"]["allowPrivateNetwork"],
            max_age=data["cors"]["maxAge"],
        )
