import httpx

from ..runtime.proxy import ProxySettings

class HTTPAsyncClientManager:

    def __init__(self, *, settings: ProxySettings) -> None:
        self.settings = settings
        self.client: httpx.AsyncClient | None = None

    async def startup(self):
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(self.settings.default_timeout),
            follow_redirects=self.settings.follow_redirects
        )

    async def shutdown(self):
        if self.client:
            await self.client.aclose()