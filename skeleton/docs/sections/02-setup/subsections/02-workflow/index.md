## Workflow

Skeleton provides individual commands for managing the application lifecycle.

### Configure

```bash
skeleton --config --profile <profile>
```

Generates project configuration files for the selected frontend profile.

### Initialize

```bash
skeleton --init
```

Creates the application structure from the framework's boilerplate.

### Install

```bash
skeleton --install
```

Installs frontend and backend dependencies.

### Start

```bash
skeleton --start
```

Starts the configured application services.

### Common Flags

Most commands support additional execution flags:

| Flag        | Purpose                                         |
|-------------|-------------------------------------------------|
| `--dry`     | Previews an operation without applying changes. |
| `--verbose` | Displays additional execution information.      |

Flags are command-specific. Use `--help` to inspect their availability.