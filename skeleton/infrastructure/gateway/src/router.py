from skeleton.infrastructure.common.src.context import RuntimeContext
from skeleton.infrastructure.gateway.src.schemas import RouteContext, UpstreamContext

class ProxyRouter:

    def __init__(self, context: RuntimeContext):

        schemas = context.config.schemas["schemas"]
        http = schemas["http"]
        ws = schemas["ws"]

        # print(http)
        # print(ws)

        # index.html file name configurable by:
        # skeleton/app/frontend/webpack/config.json
        self.index = context.config.frontend["entry"]["index"]

        backend = context.config.servers["servers"]["backend"]
        frontend = context.config.servers["servers"]["frontend"]

        self.backend = RouteContext(
            prefix=http["backend"]["prefix"],
            target=f"http://{backend['host']}:{backend['port']}",
            strip=http["backend"]["strip"],
            protocol="http",
        )

        self.frontend = RouteContext(
            prefix=http["frontend"]["prefix"],
            target=f"http://{frontend['host']}:{frontend['port']}",
            strip=http["frontend"]["strip"],
            protocol="http",
        )

        self.websock = RouteContext(
            prefix=ws["backend"]["prefix"],
            target=f"http://{backend['host']}:{backend['port']}",
            strip=http["backend"]["strip"],
            protocol="ws",
        )

    # decide where to forward/redirect
    def resolve(self, path: str) -> UpstreamContext:

        if path.startswith(self.backend.prefix):

            if self.backend.strip:
                path = path.removeprefix(self.backend.prefix)

            return UpstreamContext(
                target=self.backend.target,
                path=path,
                protocol=self.backend.protocol,
            )
        
        if path.startswith(self.websock.prefix):

            if self.websock.strip:
                path = path.removeprefix(self.websock.prefix)

            return UpstreamContext(
                target=self.websock.target,
                path=path,
                protocol=self.websock.protocol,
            )
        
        # Every other shape routes to frontend SPA!
        return UpstreamContext(
            target=self.frontend.target,
            path=path,
            protocol=self.frontend.protocol,
        )
    