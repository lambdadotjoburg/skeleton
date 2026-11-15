import dataclasses

from uuid import uuid4

from fastapi import (FastAPI, Request)

from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from ..layout.server import ServerLayout

# TODO:
# Register WebSocket routes.

def create_app(*, layout: ServerLayout) -> FastAPI:

    from .router import ProxyRouter
        
    from .client import ProxyClient

    from .reverseproxy import ReverseProxy

    from .lifespan import HTTPAsyncClientManager

    http = HTTPAsyncClientManager(settings=layout.proxy.settings)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await http.startup()
        try:
            yield
        finally:
            await http.shutdown()

    # ------------------------------------------------
    # Documentation configuration.
    # ------------------------------------------------

    from ..runtime.server import ServerName

    docs = layout.portal.service(ServerName.GATEWAY).docs

    docs_url = None
    redoc_url = None
    openapi_url = None

    if docs and docs.enabled:

        url = "/" + docs.url.strip("/")

        openapi_url = f"{url}/openapi.json"

        if docs.interface == "docs":
            docs_url = url

        elif docs.interface == "redoc":
            redoc_url = url

        else:
            raise ValueError(
                f"Unsupported documentation interface: "
                f"{docs.interface!r}"
            )

    # ------------------------------------------------
    # FastAPI application.
    # ------------------------------------------------

    app = FastAPI(
        
        lifespan=lifespan,
        title="Skeleton Server",
        description="Reverse Proxy Gateway Server",

        docs_url=docs_url,
        redoc_url=redoc_url,
        openapi_url=openapi_url,

        # version="0.0.1",
        swagger_ui_parameters={
            "docExpansion": "none",
            "displayRequestDuration": True,
            "defaultModelsExpandDepth": -1,
        },
    )

    # ------------------------------------------------
    # Middleware.
    # ------------------------------------------------

    app.add_middleware(
        CORSMiddleware,
        **dataclasses.asdict(
            layout.proxy.cors
        )
    )

    # ------------------------------------------------
    # Proxy components.
    # ------------------------------------------------

    router = ProxyRouter(layout=layout)

    client = ProxyClient(http)

    reverseproxy = ReverseProxy(
        router=router,
        client=client,
    )

    # ------------------------------------------------
    # HTTP routes.
    # ------------------------------------------------

    devtools_uuid = str(uuid4())

    @app.get(
        "/.well-known/appspecific/com.chrome.devtools.json",
        tags=["devtools"],
        summary=(
            "Chrome devtools automatic workspace request"
        ),
        description=(
            "Used by chrome devtools to "
            "map files loaded in browser to "
            "local project!"
        )
    )
    async def chrome_devtools():
        return JSONResponse(
            {
                "workspace": {
                    "root": str(layout.client.root),
                    "uuid": devtools_uuid,
                },
            }
        )

    @app.get(
        "/ping",
        tags=["ping"],
        summary=(
            "ping check endpoint!"
        ),
        description=(
            "Used by skeleton engine/orchestrator "
            "to ensure readiness upon gateway launch!"
        ),
    )
    async def ping():
        return {"status": "ok"}

    # @app.api_route(
    #     "/{path:path}",
    #     methods=layout.proxy.methods,
    #     # include_in_schema=False, # NOT unique!
    # )

    async def http_gateway(request: Request):

        return await reverseproxy.handle_http_request(
            request=request
        )

    for method in layout.proxy.methods:

        app.add_api_route(
            "/{path:path}",
            http_gateway,
            methods=[method],
            name=f"http_gateway_{method.lower()}",
            tags=["Skeleton Gateway Server"],
            summary=(
                f"Gateway {method} API endpoint!"
            ),
            description=(
                f"Forward the incoming {method} request "
                "to the approppriate upstream service."
            ),
        )

    return app