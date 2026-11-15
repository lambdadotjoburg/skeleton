import asyncio

from pathlib import Path

from watchfiles import awatch

from .stop import stop_process
from .start import start_backend
from .readiness import wait_for_backend

from ..layout.engine import EngineLayout

async def watch_backend(
    *,
    engine: EngineLayout,
    processes: dict[str, asyncio.subprocess.Process],
) -> None:

    reload = engine.reload

    try:

        if not reload.enabled:
            await processes["backend"].wait()
            return

        directories = [
            engine.client.backend.root / directory
            for directory in reload.directories
        ]

        if not directories:
            raise ValueError(
                "Backend reload is enabled, "
                "but no watch directories are configured."
            )

        missing = [
            directory
            for directory in directories
            if not directory.is_dir()
        ]

        if missing:
            raise NotADirectoryError(
                "Backend watch directories not found:\n"
                + "\n".join(
                    f"  - {directory}"
                    for directory in missing
                )
            )

        extensions = {
            extension.lower()
            for extension in reload.extensions
        }

        async for changes in awatch(
            *directories,
            watch_filter=lambda change, path: (
                Path(path).suffix.lower() in extensions
            ),
            debounce=300,
            step=50,
        ):

            print(
                "\nBackend changes detected. Restarting ...\n",
                flush=True,
            )

            for _, path in changes:
                print(f"  {path}", flush=True)

            await stop_process(processes["backend"])

            processes["backend"] = await start_backend(engine)

            await wait_for_backend(
                processes["backend"],
                engine,
            )

    finally:
        # The coordinator owns final process cleanup.
        pass