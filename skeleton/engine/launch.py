import asyncio

from .start import (
    start_gateway,
    start_frontend,
    start_backend,
)

from .readiness import (
    wait_for_gateway,
    wait_for_backend,
    wait_for_frontend,
)

from .stop import stop_services
from .watch import watch_backend

from .info import print_client_urls
from .portal import open_portal

from ..layout.engine import EngineLayout

async def launch(
    *,
    engine: EngineLayout
) -> int:

    processes: dict[
        str,
        asyncio.subprocess.Process
    ] = {}

    try:
        print("running skeleton orchestrator ...")

        processes["gateway"] = await start_gateway(engine)
        await wait_for_gateway(processes["gateway"], engine)

        processes["frontend"] = await start_frontend(engine)
        await wait_for_frontend(processes["frontend"], engine)

        processes["backend"] = await start_backend(engine)
        await wait_for_backend(processes["backend"], engine)

        print_client_urls(engine=engine)
        open_portal(engine=engine)

        await watch_backend(
            engine=engine,
            processes=processes,
        )

        return 0

    finally:

        print("Gracefully Terminating Skeleton Processes ...", flush=True)
        await stop_services(processes)