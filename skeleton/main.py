import sys

from pathlib import Path

from .constants.command import COMMAND_ATTRIBUTE

def cli(root: Path | None = None) -> int:

    from .layout.client import ClientLayout
    from .layout.framework import FrameworkLayout

    if root is None:
        root = Path(
            __file__
        ).resolve().parents[1]

    cwd = Path.cwd().resolve()
    root = root.resolve()

    # Determine whether executing from framework root.
    framework_dev = cwd == root

    client = None
    framework = FrameworkLayout(root=root)

    if not framework_dev:
        client = ClientLayout(root=cwd)

    from .bootstrap.venv import in_virtual_environment
    
    if not in_virtual_environment():

        from .bootstrap.notice import advisory
        from .bootstrap.notice import activation

        print(advisory())
        print(activation())

        return 1

    if framework_dev:

        from .bootstrap.dependencies import dependencies

        missing = dependencies(root, dev=True)

        if missing:
            from .bootstrap.notice import feedback

            print(feedback(missing))
            return 1

    from .plugins.loader import loader
    from .plugins.filter import decorated
    from .context.context import CLIContext

    context = CLIContext(
        cwd=cwd,
        root=cwd,
        CLIENT=client,
        FRAMEWORK=framework,
    )

    registry = context.REGISTRY

    # Discover framework commands.
    for module in loader(
        directory=framework.CLI,
        root=framework.root,
        filter=decorated("command"),
    ):
        registry.discover(
            module,
            attribute=COMMAND_ATTRIBUTE
        )

    # when operating as client!
    if client and client.config.exists("skeleton-project.json"):

        if client.plugins.is_dir():

            # Discover client plugins,
            for module in loader(
                directory=client.plugins,
                root=client.root,
                filter=decorated("command"),
            ):
                registry.discover(
                    module,
                    attribute=COMMAND_ATTRIBUTE
                )

    return registry.invoke(
        args=sys.argv[1:],
        context=context,
    )