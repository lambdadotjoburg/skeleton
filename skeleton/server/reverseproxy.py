from fastapi import Request

from urllib.parse import urljoin

from fastapi.responses import StreamingResponse

from .client import ProxyClient
from .router import ProxyRouter

from .schemas import UpstreamRequest

# from pathlib import PurePosixPath

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

class ReverseProxy:
    
    def __init__(
            self,
            router: ProxyRouter,
            client: ProxyClient
        ):
        self.router = router
        self.client = client

    async def handle_http_request(
        self,
        request: Request,
    ) -> StreamingResponse:
        
        upstream = self.router.resolve(request.url.path)

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
