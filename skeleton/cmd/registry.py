from collections.abc import Iterator

import dataclasses
from typing import Generic

from types import ModuleType

from .parser import parse

from .command import Command

from .types import AuthProtocol

from .types import ContextT

class CommandRegistry(Generic[ContextT]):

    def __init__(
        self,
        *,
        context: ContextT,
        authorizer: AuthProtocol | None = None,
    ) -> None:

        self.context = context
        self.authorizer = authorizer
        self.commands: dict[str, Command[ContextT]] = {}

    def __iter__(self) -> Iterator[Command[ContextT]]:

        return iter(self.commands.values())

    def get(self, name: str) -> Command[ContextT] | None:
        
        return self.commands.get(name)

    def register(
        self,
        command: Command[ContextT],
    ) -> None:

        # if command.name in self.commands:
        #     raise ValueError(
        #         f"Duplicate command: {command.name}"
        #     )

        # self.commands[command.name] = command

        definition = command.resolve(self.context)
        name = definition.name

        if name in self.commands:
            raise ValueError(
                f"Duplicate command: {name}"
            )

        self.commands[name] = command

    def discover(
        self,
        module: ModuleType,
        *,
        attribute: str,
    ) -> None:

        for member in vars(module).values():

            if getattr(
                member,
                "__module__",
                None
            ) != module.__name__:
                continue

            metadata = getattr(
                member,
                attribute,
                None,
            )

            if isinstance(metadata, Command):
                self.register(metadata)

    def invoke(
        self, 
        *,
        args: list[str],
        context: ContextT,
    ):
        if not args:
            raise ValueError("No command specified.")

        token = args[0]

        if not token.startswith("--") or token == "--":
            raise ValueError(
                f"Expected a command name, got: {token}"
            )

        name = token.removeprefix("--")

        command = self.commands.get(name)

        if command is None:
            raise ValueError(f"Unknown command: {token}")

        if self.authorizer is not None:
            self.authorizer.authorize(command)

        definition = command.resolve(context)

        parser = command.parser or parse

        values = parser(
            definition,
            args[1:],
        )

        return command.execute(
            values=values,
            context=context,
        )