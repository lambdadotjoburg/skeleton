from collections.abc import Callable

from .context import CLIContext

from .roles import Role

from .mode import Mode

Predicate = Callable[[CLIContext], bool]

predicates: dict[str, Predicate] = {

    Role.CLIENT: lambda context: (
        context.mode is Mode.CLIENT
    ),
    
    Role.FRAMEWORK: lambda context: (
        context.mode is Mode.FRAMEWORK
    ),
}