from ..layout.server import ServerLayout

from .schemas import (RouteContext, UpstreamContext)

class ProxyRouter:
        
    def __init__(self, layout: ServerLayout):

        from ..runtime.server import ServerName

        schemas = layout.schemas

        frontend = layout.server(ServerName.FRONTEND)
        backend = layout.server(ServerName.BACKEND)
        # websocket = layout.servers.websocket

        self.backend = RouteContext(
            prefix=schemas.http.backend.prefix,
            target=f"http://{backend.host}:{backend.port}",
            strip=schemas.http.backend.strip,
            protocol="http",
        )

        self.frontend = RouteContext(
            prefix=schemas.http.frontend.prefix,
            target=f"http://{frontend.host}:{frontend.port}",
            strip=schemas.http.frontend.strip,
            protocol="http",
        )

        # self.websocket = RouteContext(
        #     prefix=schemas.ws.backend.prefix,
        #     target=f"http://{backend.host}:{backend.port}",
        #     strip=schemas.ws.backend.strip,
        #     protocol="ws",
        # )

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
        
        # if path.startswith(self.websocket.prefix):
        #
        #     if self.websocket.strip:
        #         path = path.removeprefix(self.websocket.prefix)
        #
        #     return UpstreamContext(
        #         target=self.websocket.target,
        #         path=path,
        #         protocol=self.websocket.protocol,
        #     )
        
        # Every other shape routes to frontend SPA!
        return UpstreamContext(
            target=self.frontend.target,
            path=path,
            protocol=self.frontend.protocol,
        )
