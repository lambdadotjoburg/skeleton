import asyncio

from pathlib import Path
from asyncio.subprocess import Process

from skeleton.infrastructure.gateway.src.context import ServiceContext

# actual runtime services!
class Service:

    def __init__(self, config: ServiceContext):
        
        self.config = config
        self.proc: Process | None = None

        self.watch_task: asyncio.Task | None = None

        # avoid race conditions & multiple restarts
        self.restart_lock = asyncio.Lock()

    async def run(self) -> None:
        await self.start()
        self.watch_task = asyncio.create_task(self.watch_loop())

    async def start(self) -> None:

        print(
            f"INFO:     Starting {self.config.name}"
            f" at http://{self.config.network.host}:"
            f"{self.config.network.port}"
        )

        self.proc = await asyncio.create_subprocess_exec(
            self.config.process.exe, "-m", "uvicorn",
            f"{self.config.process.module}:{self.config.name}",
            "--host", f"{self.config.network.host}",
            "--port", f"{self.config.network.port}",
            cwd=self.config.process.cwd,
        )

    # This loop runs forever ...
    async def watch_loop(self) -> None:

        print(
            f"INFO      {self.config.name}"
            f" hot-module reload {self.config.watch.enabled}"
        )

        if not self.config.watch.enabled:
            return
        
        # lazy import awatch!
        from watchfiles import awatch # type: ignore
        
        try:
            async for changes in awatch(self.config.watch.directory):
                # check whether changes contains a file having extension
                # that corresponds to any of the extensions in the config list!
                if any(
                    Path(path).suffix
                    in self.config.watch.extensions
                    for _, path in changes
                ):
                    await asyncio.sleep(0.25)
                    await self.restart()

        except asyncio.CancelledError:
            raise

    # proper cleanup needed!
    async def stop(self) -> None:
        # check: does subprocess exist? + still running? (return code None)
        if self.proc is not None and self.proc.returncode is None:
            print(
                f"INFO:     Terminating "
                f"{self.config.name} at "
                f"{self.config.network.host} on "
                f"{self.config.network.port}"
            )
            self.proc.terminate()
            await self.proc.wait()

    # context manager in restart() is equivalent but safer:
    # 
    #   await self.restart_lock.acquire()
    # 
    #   try:
    #       await self.stop()
    #       await self.start()
    # 
    #   finally:
    #       self.restart_lock.release()
    # 
    #   # async with context manager is safer
    async def restart(self) -> None:
        # async mutex lock => prevent multiple restarts!
        # ONLY ONE coroutine may enter this block at any instance!
        async with self.restart_lock:
            print(
                f"INFO:     Restarting "
                f"{self.config.name} at "
                f"{self.config.network.host} on "
                f"{self.config.network.port}"
            )
            await self.stop()
            await self.start()

    async def shutdown(self):

        # cancel watcher tasks FIRST!
        if self.watch_task:

            self.watch_task.cancel()

            try:
                await self.watch_task
            except asyncio.CancelledError:
                pass

        # THEN terminate subprocess!
        await self.stop()
        print("INFO:     Graceful shutdown complete!")
        