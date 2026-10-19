import httpx

class HTTPAsyncClientManager:

    def __init__(self, config: dict) -> None:
        self.config = config
        self.client: httpx.AsyncClient | None = None

    async def startup(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.config["defaultTimeout"]),
            follow_redirects=self.config["followRedirects"]
        )

    async def shutdown(self):
        if self.client:
            await self.client.aclose()