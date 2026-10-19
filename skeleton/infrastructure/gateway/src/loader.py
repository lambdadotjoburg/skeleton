from pathlib import Path

from skeleton.infrastructure.common.src.context import RuntimeContext

from skeleton.infrastructure.gateway.src.utils import normalize_extensions

from skeleton.infrastructure.common.src.utils import (
    path_to_module, resolve_executable_path
)

from skeleton.infrastructure.gateway.src.context import (
    NetworkContext, ProcessContext,
    ServiceContext, WatchContext
)

from skeleton.infrastructure.gateway.src.config import (
    NetworkConfig, ProcessConfig,
    ServiceConfig, WatchConfig
)

def load_service_configs(
    context: RuntimeContext
) -> list[ServiceConfig]:
    
    configs: list[ServiceConfig] = []
    
    servers = context.config.servers["servers"]
    services = context.config.services["services"]
    
    # use services to get the relevant server for that service:
    for name, service in services.items():

        networkConfig = NetworkConfig(
            host=servers[name]["host"],
            port=servers[name]["port"],
        )

        watchConfig = WatchConfig(
            enabled=service["reload"],
            extensions=service["ext"],
        )

        if name == "backend":

            service_root = context.layout.backend

            module_path = service_root / "src" / "main.py"

            module = path_to_module(module_path.relative_to(service_root))

        else:

            service_root = context.root / service["root"]
            module = service["module"]

        processConfig = ProcessConfig(
            module=module
        )

        configs.append(
            ServiceConfig(
                root=service_root,
                id=name,
                name=service["name"],
                network=networkConfig,
                watch=watchConfig,
                process=processConfig,
            )
        )

    return configs

# build the immutable/frozen
# service configuration objects
def build_service_contexts(
    configs: list[ServiceConfig]
) -> list[ServiceContext]:
    
    contexts: list[ServiceContext] = []

    for config in configs:

        process = ProcessContext(
            module=config.process.module,
            exe=resolve_executable_path(config.root),
            cwd=Path(config.root),
        )

        network = NetworkContext(
            host=config.network.host,
            port=config.network.port,
        )
        
        watch = WatchContext(
            enabled=config.watch.enabled,
            directory=config.root,
            extensions=normalize_extensions(
                config.watch.extensions
            ),
        )

        contexts.append(
            ServiceContext(
                id=config.id,
                name=config.name,
                root=config.root,
                process=process,
                network=network,
                watch=watch,
            )
        )

    return contexts
