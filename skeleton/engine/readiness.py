import asyncio

import urllib.error
import urllib.request

from ..layout.engine import EngineLayout
from ..runtime.server import ServerName

TIMEOUT = 60
INTERVAL = 0.25

async def service_is_ready(url: str) -> bool:

    def request() -> bool:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                return 200 <= response.status < 300

        except (urllib.error.URLError, TimeoutError, OSError):
            return False

    return await asyncio.to_thread(request)

async def wait_for_service(
    process: asyncio.subprocess.Process,
    url: str,
    *,
    name: str,
    timeout: float = TIMEOUT,
) -> None:

    deadline = asyncio.get_running_loop().time() + timeout

    while asyncio.get_running_loop().time() < deadline:

        if process.returncode is not None:
            raise RuntimeError(
                f"{name} process exited before becoming ready "
                f"(exit code: {process.returncode})."
            )

        if await service_is_ready(url):
            return

        await asyncio.sleep(INTERVAL)

    raise TimeoutError(
        f"{name} did not become ready within {timeout} seconds: {url}"
    )

async def wait_for_gateway(
    process: asyncio.subprocess.Process,
    engine: EngineLayout,
) -> None:

    server = engine.server.server(ServerName.GATEWAY)

    # cannot use openapi.json endpoint to check for readiness,
    # because the client's configuration controls whether or not
    # the gateway's documentation is enabled, and if not, then
    # the readiness-check won't work, obviously, so we use a
    # dedicated "ping" endpoint instead!

    # await wait_for_service(
    #     process,
    #     f"http://{server.host}:{server.port}/openapi.json",
    #     name="Gateway",
    # )

    await wait_for_service(
        process,
        f"http://{server.host}:{server.port}/ping",
        name="Gateway",
    )

async def wait_for_frontend(
    process: asyncio.subprocess.Process,
    engine: EngineLayout,
) -> None:

    server = engine.server.server(ServerName.FRONTEND)

    await wait_for_service(
        process,
        f"http://{server.host}:{server.port}/",
        name="Frontend",
    )

async def wait_for_backend(
    process: asyncio.subprocess.Process,
    engine: EngineLayout,
) -> None:

    server = engine.server.server(ServerName.BACKEND)

    await wait_for_service(
        process,
        f"http://{server.host}:{server.port}/openapi.json",
        name="Backend",
    )
