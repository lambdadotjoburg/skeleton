from typing import Any

from ..cmd.command import Command

from ..context.context import CLIContext

def available(
    command: Command,
    context: CLIContext
) -> bool:

    authorizer = context.REGISTRY.authorizer

    if authorizer is None:
        return not command.roles

    return authorizer.permits(command)

def help(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    registry = context.REGISTRY
    
    commands = values.get("commands", [])

    print("\nSkeleton\n")

    if commands:

        for name in commands:

            command = registry.get(name)

            if command is None:
                print(f"Unknown command: --{name}")
                return 2

            if not available(command, context):
                print(
                    f"Command '--{name}' is not available "
                    f"in {context.mode} mode."
                )
                return 2

            print(
                f"--{command.name}\n"
                f"\t{command.definition.description}\n"
                f"\tUsage: {command.usage()}\n"
            )

        return 0

    print("Usage:\n\tskeleton --<command> [options]\n")
    print("Commands:\n")

    for command in registry:

        if available(command, context):
            print(
                f"\t--{command.name}: "
                f"{command.definition.description}"
            )

    return 0
