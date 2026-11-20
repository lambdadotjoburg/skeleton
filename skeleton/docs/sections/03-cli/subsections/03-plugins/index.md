## Plugins

Skeleton supports client-defined CLI commands via plugins.

Plugins are Python modules placed inside
the client's configured plugin directory.

The default directory is `plugins/`, as specified by
the `plugins` entry in `config/skeleton-project.json`.

### Creating a command

Use the `@command` decorator to register a custom command.

```python
from skeleton.cmd.types import Values
from skeleton.cmd.command import Command
from skeleton.context.context import CLIContext
from skeleton.decorators.command import command

@command(
    name="custom-client-command",
    factory=lambda context: Command.Definition(
        name="custom-client-command",
        description="Custom command using client context!",
        arguments={"arg": "*"},
    ),
)
def custom_client_command(
    *,
    values: Values,
    context: CLIContext,
) -> int:
    print(context.root)
    print(values["arg"])
    return 0
```

## Discovery

Skeleton recursively discovers Python modules
inside the configured plugin directory.

Modules containing a `@command` declaration are imported
and their commands are registered with the CLI.

This allows client projects to add custom commands
without modifying the framework itself.