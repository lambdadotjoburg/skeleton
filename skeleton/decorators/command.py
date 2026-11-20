from collections.abc import Callable

from skeleton.cmd.types import DefinitionFactory

from ..cmd.command import Command

from ..cmd.types import Arguments
from ..cmd.types import ParserProtocol

from ..context.roles import Role
from ..context.context import CLIContext

from typing import ParamSpec, TypeAlias

from ..constants.command import COMMAND_ATTRIBUTE

CLICommandFactory: TypeAlias = DefinitionFactory[CLIContext]

P = ParamSpec("P")

def command(
    *,
    name: str | None = None,
    description: str = "",
    flags: list[str] | None = None,
    arguments: dict[str, Arguments] | None = None,
    defaults: dict[str, str | bool | list[str] | None] | None = None,
    parser: ParserProtocol | None = None,
    factory: CLICommandFactory | None = None,
    roles: list[str] | None = None,
) -> Callable[[Callable[P, int]], Callable[P, int]]:

    def decorate(
        action: Callable[P, int],
    ) -> Callable[P, int]:

        if factory is None:

            if name is None:
                raise ValueError(
                    "command name is required without a factory."
                )

            # Construct the command definition.
            definition = Command.Definition(
                name=name,
                description=description,
                flags=flags or [],
                arguments=arguments or {},
                defaults=defaults or {},
            )

        else:
            definition = None
            
        # Construct the command metadata.
        metadata = Command(
            action=action,
            parser=parser,
            definition=definition,
            roles=roles if roles is not None else [Role.CLIENT],
            factory=factory,
        )

        # Attach metadata to
        # the original function.
        setattr(
            action,
            COMMAND_ATTRIBUTE,
            metadata,
        )

        return action

    return decorate
