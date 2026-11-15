import sys, uvicorn

from pathlib import Path

from ..cmd.command import Command
from ..runtime.mode import RuntimeMode
from ..runtime.server import ServerName

CMD_DEF_SERVER = Command.Definition(

    description="start skeleton reverse proxy gateway",

    arguments={
        
        "root": "*",
        "cwd": "*",

        "mode": [
            mode.value
            for mode in RuntimeMode
        ],
    },

    defaults={ "mode": None }
)

def main() -> int:

    from ..cmd.parser import parse

    from ..layout.client import ClientLayout
    from ..layout.server import ServerLayout

    from .app import create_app

    values = parse(
        CMD_DEF_SERVER,
        sys.argv[1:],
    )

    root = values["root"]
    cwd = values["cwd"]
    mode = values["mode"]

    if not isinstance(root, str):
        raise ValueError("Invalid server root.")

    if not isinstance(cwd, str):
        raise ValueError("Invalid client root.")

    if not isinstance(mode, str):
        raise ValueError("Invalid runtime mode.")

    client=ClientLayout(root=Path(cwd))
    client.runtime.mode = RuntimeMode(mode)

    layout = ServerLayout(
        root=Path(root),
        client=client,
    )

    gateway = layout.server(ServerName.GATEWAY)

    app = create_app(layout=layout)

    uvicorn.run(
        app,
        host=gateway.host,
        port=gateway.port,
    )

    return 0

if __name__ == "__main__":
    raise SystemExit(main())