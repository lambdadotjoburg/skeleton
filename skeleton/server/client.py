import httpx

from fastapi import Request

from fastapi.responses import StreamingResponse

from starlette.background import BackgroundTask

from .schemas import UpstreamRequest

from .lifespan import HTTPAsyncClientManager

from .headers import HOP_BY_HOP_HEADERS

class ProxyClient:

    def __init__(self, manager: HTTPAsyncClientManager):
        self.manager = manager

    @property
    def client(self) -> httpx.AsyncClient:
        if self.manager.client is None:
            raise RuntimeError("HTTP client has not been started.")

        return self.manager.client

    def filter_hop_by_hop_headers(
        self,
        headers: list[tuple[bytes, bytes]],
    ) -> list[tuple[bytes, bytes]]:

        # Identify headers nominated by Connection.
        blocked_headers = {
            name.encode("ascii")
            for name in HOP_BY_HOP_HEADERS
        }

        for name, value in headers:
            if name.lower() == b"connection":
                blocked_headers.update(
                    header.strip().lower()
                    for header in value.split(b",")
                )

        # Preserve all remaining raw header pairs.
        return [
            (name, value)
            for name, value in headers
            if name.lower() not in blocked_headers
        ]

    async def request(
        self,
        client_request: UpstreamRequest,
    ) -> StreamingResponse:

        request: Request = client_request.request

        # Filter incoming request headers.
        headers = self.filter_hop_by_hop_headers(
            request.headers.raw
        )

        # Remove incoming Host; HTTPX generates its own.
        headers = [
            (name, value)
            for name, value in headers
            if name.lower() != b"host"
        ]

        # Build outgoing request.
        outgoing_request = self.client.build_request(
            method=request.method,
            url=client_request.target,
            headers=headers,
            content=request.stream(),
        )

        # Send request and stream upstream response.
        upstream_response = await self.client.send(
            outgoing_request,
            stream=True,
        )

        # Filter upstream response headers.
        filtered_headers = self.filter_hop_by_hop_headers(
            upstream_response.headers.raw
        )

        response = StreamingResponse(
            upstream_response.aiter_raw(),
            status_code=upstream_response.status_code,
            background=BackgroundTask(
                upstream_response.aclose
            ),
        )

        # Preserve duplicate response headers.
        response.raw_headers = filtered_headers

        return response