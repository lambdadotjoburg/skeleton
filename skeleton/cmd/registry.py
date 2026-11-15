from collections.abc import Iterator

from .parser import parse

from .command import Command

from .types import AuthProtocol

class CommandRegistry():

    def __init__(
        self,
        commands: list[Command],
        *,
        authorizer: AuthProtocol | None = None,
    ) -> None:

        self.authorizer = authorizer

        self.commands: dict[str, Command] = {}

        for command in commands:

            if command.name in self.commands:
                raise ValueError(
                    f"Duplicate command: {command.name}"
                )

            self.commands[command.name] = command

    def __iter__(self) -> Iterator[Command]:

        return iter(self.commands.values())

    def get(self, name: str) -> Command | None:
        
        return self.commands.get(name)

    def invoke(
        self, 
        *,
        args: list[str],
        context: object,
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

        parser = command.parser or parse

        values = parser(
            command.definition,
            args[1:],
        )

        return command.execute(
            values=values,
            context=context,
        )