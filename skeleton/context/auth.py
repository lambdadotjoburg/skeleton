from ..cmd.command import Command

from .context import CLIContext
from .predicates import Predicate

class Authorization:

    def __init__(
        self,
        *,
        context: CLIContext,
        predicates: dict[str, Predicate],
    ) -> None:

        self.context = context
        self.predicates = predicates

    def permits(self, command: Command) -> bool:

        if not command.roles:
            return True

        for role in command.roles:

            predicate = self.predicates.get(role)

            if predicate is not None and predicate(self.context):
                return True

        return False

    def authorize(self, command: Command) -> None:

        if not self.permits(command):
            raise PermissionError(
                f"Command '--{command.name}' is not permitted."
            )