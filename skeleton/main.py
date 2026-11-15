import sys

from pathlib import Path

from .environment.dependencies import dependencies
from .environment.resolver import in_virtual_environment

def cli(root: Path | None = None) -> int:

    framework_dev = root is not None

    from .context.mode import Mode
    from .context.predicates import predicates

    from .context.context import CLIContext
    from .context.auth import Authorization

    from .layout.framework import FrameworkLayout
    from .register import create_registry

    if root is None:
        root = Path(__file__).resolve().parents[1]

    cwd = Path.cwd().resolve()
    root = root.resolve()

    # cwd = Path.cwd().resolve()
    # root = root.resolve()

    framework = FrameworkLayout(root=root)

    registry = create_registry(framework)

    context = CLIContext(
        cwd=cwd,
        root=cwd,
        REGISTRY=registry,
        FRAMEWORK=framework,
    )

    if not in_virtual_environment():

        from .environment.notice import advisory
        from .environment.notice import activation

        print(advisory())
        print(activation())

    if framework_dev:

        missing = dependencies(root, dev=True)

        if missing:
            from .environment.notice import feedback

            print(feedback(missing))
            return 1

    registry.authorizer = Authorization(
        context=context,
        predicates=predicates,
    )

    return registry.invoke(
        args=sys.argv[1:],
        context=context,
    )