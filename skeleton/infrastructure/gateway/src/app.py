from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from skeleton.infrastructure.common.src.context import RuntimeContext

from skeleton.infrastructure.gateway.src.router import ProxyRouter
from skeleton.infrastructure.gateway.src.client import ProxyClient
from skeleton.infrastructure.gateway.src.reverseproxy import ReverseProxy
from skeleton.infrastructure.gateway.src.lifespan import HTTPAsyncClientManager

from contextlib import asynccontextmanager

from skeleton.infrastructure.gateway.src.utils import build_static_dir

def create_app(context: RuntimeContext) -> FastAPI:

    # print(context.config.frontend["lib"]["static"])
    http = HTTPAsyncClientManager(
        context.config.proxy["settings"]
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await http.startup()
        yield
        await http.shutdown()

    reverseproxy = FastAPI(
        # name="Reverse Proxy Dev Gateway",
        title="Reverse Proxy Dev Gateway",
        description="Reverse Proxy Dev Gateway",
        version="1.0.0",
        lifespan=lifespan,
        swagger_ui_parameters={
            "docExpansion": "none",
            "displayRequestDuration": True,
            "defaultModelsExpandDepth": -1
        },
    )

    CORS = context.config.proxy["cors"]
    # set cors headers dynamically!
    reverseproxy.add_middleware(
        CORSMiddleware,
        allow_origins=CORS["allowOrigins"],
        allow_credentials=CORS["allowCredentials"],
        allow_methods=CORS["allowMethods"],
        allow_headers=CORS["allowHeaders"],
    )

    router = ProxyRouter(context=context)

    client = ProxyClient(http)
    proxy = ReverseProxy(router, client)

    from fastapi.staticfiles import StaticFiles
    static_dir = build_static_dir(context)

    print("Mounting static directory:")
    print("  URL:      ", f"/{context.config.frontend['lib']['static']}")
    print("  directory:", static_dir)
    
    reverseproxy.mount(
        f"/{context.config.frontend["lib"]["static"]}",
        StaticFiles(
            directory=str(static_dir),
            check_dir=True
            ),
        name="static"
    )

    devtools_uuid = str(uuid4())

    @reverseproxy.get("/.well-known/appspecific/com.chrome.devtools.json")
    async def chrome_devtools():
        return JSONResponse(
            {
                "workspace": {
                    "root": str(context.root),
                    "uuid": devtools_uuid,
                },
            }
        )

    METHODS = context.config.proxy["methods"]
    @reverseproxy.api_route(
        "/{path:path}",
        methods=METHODS,
        summary="http",
        tags=["http"],
    )
    async def http_gateway(request: Request):
        return await proxy.handle_http_request(request=request)
    
    return reverseproxy