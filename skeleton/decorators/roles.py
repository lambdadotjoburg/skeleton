from collections.abc import Callable

from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def roles(
    values: str | list[str]
) -> Callable[[Callable[P, R]], Callable[P, R]]:

    def decorate(action: Callable[P, R]) -> Callable[P, R]:

        normal = [values] if isinstance(values, str) else values

        setattr(action, "roles", normal)

        return action

    return decorate

def client(action: Callable[P, R]) -> Callable[P, R]:
    return roles("client")(action)

def framework(action: Callable[P, R]) -> Callable[P, R]:
    return roles("framework")(action)