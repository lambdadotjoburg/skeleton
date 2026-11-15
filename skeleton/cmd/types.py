from __future__ import annotations

from typing import Literal, TypeAlias
from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from .command import Command

Value: TypeAlias = str | bool | list[str] | None
Values: TypeAlias = dict[str, Value]

Argument: TypeAlias = list[str] | Literal["*"]
Arguments: TypeAlias = Argument # | list[Argument]

class ParserProtocol(Protocol):

    def __call__(
        self,
        definition: Command.Definition,
        tokens: list[str],
    ) -> Values: ...

class AuthProtocol(Protocol):

    def authorize(self, command: Command) -> None: ...

    def permits(self, command: Command) -> bool: ...
