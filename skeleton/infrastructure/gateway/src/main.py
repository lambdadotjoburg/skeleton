import sys, asyncio, uvicorn

from pathlib import Path

from skeleton.infrastructure.common.src.constants import Bootstrap
from skeleton.infrastructure.common.src.context import RuntimeContext
from skeleton.infrastructure.common.src.config import load_runtime_config
from skeleton.infrastructure.common.src.layout import build_layout
from skeleton.infrastructure.common.src.env import build_env

from skeleton.infrastructure.gateway.src.config import ServiceConfig
from skeleton.infrastructure.gateway.src.context import ServiceContext
from skeleton.infrastructure.gateway.src.service import Service
from skeleton.infrastructure.gateway.src.registry import Registry

from skeleton.infrastructure.gateway.src.logging import build_log_config

from skeleton.infrastructure.gateway.src.app import create_app
from skeleton.infrastructure.gateway.src.parser import parse

from skeleton.infrastructure.gateway.src.validation import (
    validate_service_configs,
    validate_service_contexts
)

from skeleton.infrastructure.gateway.src.loader import (
    build_service_contexts, load_service_configs
)

# service orchestration!
async def start(context: RuntimeContext) -> None:

    # pass in RuntimeContext
    registry = Registry()

    print("INFO:     Starting reverse proxy watchfile services ...")

    # load & build the config objects
    # configs = load_service_config(ROOT)
    serviceConfigs: list[ServiceConfig] = load_service_configs(context)
    validConfigs = validate_service_configs(serviceConfigs)

    if not validConfigs:
        exit(1)

    serviceContexts: list[ServiceContext] = build_service_contexts(serviceConfigs)
    validContexts = validate_service_contexts(serviceContexts)

    if not validContexts:
        exit(1)
    
    # log config data for visual output!
    # for name, config in configs.items():
    #     print(f"{name}:", config.to_json())
    
    # register config objects as services!
    for service in serviceContexts:
        registry.regsiter(Service(service))

    try:

        # start all services
        await registry.start_all()
        app = create_app(context)

        servers = context.config.servers["servers"]
        gateway = servers["gateway"]

        # create the uvicorn server!
        server = uvicorn.Server(
            uvicorn.Config(
                app,
                host=gateway["host"],
                port=gateway["port"],
                log_config=build_log_config(),
            )
        )

        # start the server, then ...
        # await console interrupt!
        await server.serve()

    except asyncio.CancelledError:
        print("INFO:     Stopping reverse proxy watchfile services ...")
        
    finally:
        # shutdown all services!
        await registry.stop_all()

# receive subprocess command line flags passed like:
# ['--root', 'C:\\Users\\Lambda\\Desktop\\skeleton', '--watch', '--open']
if __name__ == "__main__":

    args = sys.argv[1:]
    raw = parse(args)

    PROJECT_ROOT = Path(raw["root"]).resolve()
    FRAMEWORK_ROOT = Path(__file__).resolve().parents[4]
    MODE = raw["mode"]

    options: dict[str, str | bool] = {
        "root": str(PROJECT_ROOT),
        "mode": MODE,
        "watch": raw["watch"],
        "open": raw["open"],
    }

    layout = build_layout(
        PROJECT_ROOT / Bootstrap.LAYOUT,
        project_root=PROJECT_ROOT,
        framework_root=FRAMEWORK_ROOT,
    )

    # config = load_runtime_config(
    #     layout.common / Bootstrap.CONFIG_FILE_EXT,
    #     FRAMEWORK_ROOT,
    #     layout,
    # )

    config = load_runtime_config(
        layout.common / Bootstrap.CONFIG_FILE_EXT,
        PROJECT_ROOT,
        FRAMEWORK_ROOT,
        layout,
    )

    env = build_env(PROJECT_ROOT, MODE)

    context = RuntimeContext(
        root=PROJECT_ROOT,
        mode=MODE,
        args=args,
        env=env,
        layout=layout,
        options=options,
        config=config,
    )

    asyncio.run(start(context))