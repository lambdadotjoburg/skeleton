import dataclasses

from typing import Any, Generic

from collections.abc import Callable

from .types import ParserProtocol

from .types import Arguments, Values

from .types import ContextT

@dataclasses.dataclass(
    kw_only=True,
    frozen=True,
)
class Command(Generic[ContextT]):

    parser: ParserProtocol | None = None

    @dataclasses.dataclass(
        kw_only=True,
        frozen=True,
    )
    class Definition:

        name: str

        description: str = ""

        flags: list[str] = dataclasses.field(default_factory=list)

        arguments: dict[str, Arguments] = dataclasses.field(default_factory=dict)

        defaults: dict[str, str | bool | list[str] | None] = dataclasses.field(default_factory=dict)

    # factory: Callable[..., Definition] | None = None
    factory: Callable[[ContextT], Definition] | None = None

    definition: Definition | None = None
    
    roles: list[str] = dataclasses.field(default_factory=list)

    action: Callable[..., int]

    def __post_init__(self) -> None:

        if self.factory is None and self.definition is None:
            raise ValueError(
                "A command requires a definition or factory."
            )

        declared = getattr(self.action, "roles", [])

        merged = list(
            dict.fromkeys(
                [*self.roles, *declared]
            )
        )

        object.__setattr__(self, "roles", merged)

    @property
    def name(self) -> str:

        if self.definition is None:
            raise RuntimeError(
                "Command definition has not been resolved."
            )

        return self.definition.name

    def metadata(
        self,
        attribute: str,
        default: Any = None,
    ) -> Any:

        return getattr(self, attribute, default)

    def resolve(
        self,
        context: ContextT
    ) -> Definition:

        if self.definition is None:

            if self.factory is None:
                raise RuntimeError(
                    "Command has no definition factory."
                )

            definition = self.factory(context)

            object.__setattr__(
                self,
                "definition",
                definition,
            )

        return self.definition

    def execute(
        self, *,
        values: Values,
        context: ContextT
    ) -> int:

        return self.action(
            values=values,
            context=context,
        )

    def usage(
        self,
        definition: Definition | None = None
    ) -> str:

        if definition is None:
            if self.definition is None:
                raise RuntimeError(
                    "Command definition has not been resolved."
                )

            definition = self.definition

        parts = [f"skeleton --{self.name}"]

        for name, allowed in definition.arguments.items():

            if allowed == "*":
                argument = f"--{name.upper()} VALUE"

            elif allowed == ["*"]:
                argument = f"--{name.upper()} VALUE..."

            else:
                options = " | ".join(allowed)
                argument = f"--{name.upper()} ({options})"

            if name in definition.defaults:
                argument = f"[{argument}]"

            parts.append(f"{argument}")

        parts.extend(
            f"[--{flag}]"
            for flag in definition.flags
        )

        return " ".join(parts)
