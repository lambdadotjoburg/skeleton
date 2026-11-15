import dataclasses

from typing import Any

from collections.abc import Callable

from .types import ParserProtocol

from .types import Arguments, Values

@dataclasses.dataclass(
    kw_only=True,
    frozen=True,
)
class Command:

    parser: ParserProtocol | None = None

    @dataclasses.dataclass(
        kw_only=True,
        frozen=True,
    )
    class Definition:

        description: str = ""

        flags: list[str] = dataclasses.field(default_factory=list)

        arguments: dict[str, Arguments] = dataclasses.field(default_factory=dict)

        defaults: dict[str, str | bool | list[str] | None] = dataclasses.field(default_factory=dict)

    definition: Definition = dataclasses.field(default_factory=Definition)
    
    roles: list[str] = dataclasses.field(default_factory=list)

    action: Callable[..., int]

    def __post_init__(self) -> None:

        declared = getattr(self.action, "roles", [])

        merged = list(
            dict.fromkeys(
                [*self.roles, *declared]
            )
        )

        object.__setattr__(self, "roles", merged)

    @property
    def name(self) -> str:
        return self.action.__name__

    def metadata(
        self,
        attribute: str,
        default: Any = None,
    ) -> Any:

        return getattr(self, attribute, default)

    def execute(
        self, *,
        values: Values,
        context: object
    ) -> int:

        return self.action(
            values=values,
            context=context,
        )

    def usage(self) -> str:

        parts = [f"skeleton --{self.name}"]

        for name, allowed in self.definition.arguments.items():

            if allowed == "*":
                argument = f"--{name.upper()} VALUE"

            elif allowed == ["*"]:
                argument = f"--{name.upper()} VALUE..."

            else:
                options = " | ".join(allowed)
                argument = f"--{name.upper()} ({options})"

            if name in self.definition.defaults:
                argument = f"[{argument}]"

            parts.append(f"{argument}")

        parts.extend(
            f"[--{flag}]"
            for flag in self.definition.flags
        )

        return " ".join(parts)
