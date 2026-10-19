from fastapi import Request
from urllib.parse import urljoin

from skeleton.infrastructure.gateway.src.client import ProxyClient
from skeleton.infrastructure.gateway.src.router import ProxyRouter
from skeleton.infrastructure.gateway.src.schemas import UpstreamRequest

from pathlib import PurePosixPath

# coming from:
# http://127.0.0.1:8000/api/some/path
# resolves to:
# http://127.0.0.1:8080/some/path
# send request to Backend!

# coming from:
# http://127.0.0.1:8000/some/path
# resolves to:
# http://127.0.0.1:3000/some/path
# send request to Frontend!

def is_asset(path: str) -> bool:
    return "." in PurePosixPath(path).name

class ReverseProxy:
    
    def __init__(self, router: ProxyRouter, client: ProxyClient):
        self.router = router
        self.client = client

    async def handle_http_request(self, request: Request):

        path = request.url.path
        upstream = self.router.resolve(path)

        # SPA Fallback logic!
        if upstream.target == self.router.frontend.target:
            if not is_asset(path):
                path = f"/{self.router.index}"

        # build the target url
        target = urljoin(upstream.target, upstream.path)

        # if request has query params
        # include them for client.request!
        if request.url.query:
            target += f"?{request.url.query}"

        return await self.client.request(
            UpstreamRequest(
                request=request,
                target=target
            )
        )
