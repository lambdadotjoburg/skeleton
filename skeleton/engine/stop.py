import os
import signal
import asyncio

async def stop_process(
    process: asyncio.subprocess.Process,
) -> None:

    if process.returncode is not None:
        return

    if os.name == "nt":

        try:
            process.send_signal(signal.CTRL_BREAK_EVENT)

        except ProcessLookupError:
            await process.wait()
            return

        except OSError:
            # Graceful signalling failed; use the fallback.
            pass

        else:
            try:
                await asyncio.wait_for(
                    process.wait(),
                    timeout=5,
                )
                return

            except asyncio.TimeoutError:
                pass

        if process.returncode is not None:
            return

        task = await asyncio.create_subprocess_exec(
            "taskkill",
            "/PID", str(process.pid),
            "/T",
            "/F",
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )

        await task.wait()

        try:
            await asyncio.wait_for(
                process.wait(),
                timeout=5,
            )

        except asyncio.TimeoutError as error:
            raise RuntimeError(
                f"Could not terminate process tree "
                f"for PID {process.pid}. "
                f"taskkill exit code: {task.returncode}"
            ) from error

        if task.returncode != 0:
            raise RuntimeError(
                f"taskkill failed for PID {process.pid}. "
                f"Exit code: {task.returncode}"
            )

        return

    process.terminate()

    try:
        await asyncio.wait_for(
            process.wait(),
            timeout=5,
        )

    except asyncio.TimeoutError:
        process.kill()
        await process.wait()


async def stop_services(
    processes: dict[
        str,
        asyncio.subprocess.Process
    ],
) -> None:

    for process in reversed(
        list(processes.values())
    ):
        await stop_process(process)
