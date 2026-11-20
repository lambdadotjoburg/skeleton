## Client-defined scripts

Skeleton allows client projects to expose
their own custom npm scripts through the
command-line interface at the project root.

Define scripts in the client's `package.json`:

```json
{
    "scripts": {
        "build:packages": "tsc --build",
        "watch:packages": "tsc --build --watch",
        "clean:packages": "tsc --build --clean"
    }
}
```

Run a script through Skeleton using `--script`:

```bash
skeleton --script build:packages
skeleton --script watch:packages
skeleton --script clean:packages
```

Skeleton delegates execution to npm, invoking
the requested script from the client's project context.

This allows clients to extend Skeleton's command-line
without requiring changes to the framework's internals.

**Built-in operations remain independent.**

Commands such as `--start`, `--dist`, and `--preview`
are managed by Skeleton and do not depend on npm script.

Client projects can therefore customize `package.json` scripts
without changing the behaviour of Skeleton's built-in commands.