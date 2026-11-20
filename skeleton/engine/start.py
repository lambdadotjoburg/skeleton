import os, asyncio
import subprocess

from ..layout.engine import EngineLayout
from ..runtime.server import ServerName

async def start_gateway(
    engine: EngineLayout
) -> asyncio.subprocess.Process:

    server = engine.server
    
    print("\nStarting Skeleton Reverse Proxy Gateway ...", flush=True)

    return await asyncio.create_subprocess_exec(
        str(engine.framework.venv_python),
        "-m",
        engine.server.module,
        "--root", str(server.root),
        "--cwd", str(engine.client.root),
        "--mode", engine.client.mode.value,
        cwd=engine.framework.root,
        creationflags=(
            subprocess.CREATE_NEW_PROCESS_GROUP
            if os.name == "nt"
            else 0
        ),
    )

# "serve": "webpack serve --config webpack.config.js"
async def start_frontend(
    engine: EngineLayout,
) -> asyncio.subprocess.Process:

    from ..runtime.mode import RuntimeMode

    mode = engine.client.mode
    server = engine.server.server(ServerName.FRONTEND)

    if not engine.webpack.is_file():
        raise FileNotFoundError(
            "Webpack config not found: "
            f"{engine.webpack}"
        )

    print("\nStarting Client Frontend ...", flush=True)

    npm = engine.client.frontend.npm

    if mode == RuntimeMode.DEV:

        command = [
            npm,
            "exec",
            "--",
            "webpack",
            "serve",
            "--config", str(engine.webpack),
            "--env", f"root={engine.client.root}",
            "--env", f"mode={mode.value}",
            "--env", f"host={server.host}",
            "--env", f"port={server.port}",
            "--host", server.host,
            "--port", str(server.port),
        ]

        for key, value in engine.client.runtime.webpack.items():
            command.extend(["--env", f"{key}={value}"])

    elif mode == RuntimeMode.PREVIEW:

        command = [
            npm,
            "exec",
            "--",
            "serve",
            "-s",
            str(engine.client.frontend.outdir),
            "-l", f"tcp://{server.host}:{server.port}",
        ]

    else:
        raise ValueError(
            f"Unsupported frontend runtime mode: {mode}"
        )

    return await asyncio.create_subprocess_exec(
        *command,
        cwd=engine.client.frontend.root,
        creationflags=(
            subprocess.CREATE_NEW_PROCESS_GROUP
            if os.name == "nt"
            else 0
        ),
    )

async def start_backend(
    engine: EngineLayout
) -> asyncio.subprocess.Process:

    server = engine.server.server(ServerName.BACKEND)

    print("\nStarting Client Backend ...", flush=True)

    return await asyncio.create_subprocess_exec(
        str(engine.client.backend.venv_python),
        "-m",
        "uvicorn",
        engine.client.backend.entry,
        "--host", server.host,
        "--port", str(server.port),
        cwd=engine.client.backend.root,
        creationflags=(
            subprocess.CREATE_NEW_PROCESS_GROUP
            if os.name == "nt"
            else 0
        ),
    )