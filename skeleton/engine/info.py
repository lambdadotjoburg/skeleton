import os

from ..layout.engine import EngineLayout

SEPARATOR = "%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%"
LINEBREAK = "---------------------------------------"

def print_client_urls(engine: EngineLayout) -> None:

    servers = engine.server.servers

    # Bright cyan (light blue)
    color = "\033[96m" if "NO_COLOR" not in os.environ else ""
    reset = "\033[0m" if color else ""

    from ..runtime.server import ServerName
    
    gateway = servers[ServerName.GATEWAY]
    backend = servers[ServerName.BACKEND]
    frontend = servers[ServerName.FRONTEND]

    print(
        "\n",
        f"{color}",
        f"{SEPARATOR}\n",
        f"  SKELETON URL's\n",
        f"{LINEBREAK}\n",
        f"    Gateway:  http://{gateway.host}:{gateway.port}\n",
        f"    Backend:  http://{backend.host}:{backend.port}\n",
        f"    Frontend: http://{frontend.host}:{frontend.port}\n",
        SEPARATOR,
        f"{reset}\n",
        flush=True,
    )