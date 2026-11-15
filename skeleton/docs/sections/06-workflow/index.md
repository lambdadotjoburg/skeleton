## Workflow

The [`--quickstart`](#quickstart) command combines `--config`, `--init` & `--install`.

For more control, skeleton exposes each command separately for better workflow.

### 1. Configure

```bash
skeleton --config --profile <profile>
```

Generates the project configuration files using the selected frontend profile.

Review and customize the configuration before continuing, if necessary.

### 2. Initialize

```bash
skeleton --init
```

Creates the application structure
from the framework's boilerplate
& prepares the frontend & backend components.

### 3. Install

```bash
skeleton --install
```

Installs frontend dependencies using npm
& backend Python dependencies into
the backend virtual environment.

### 4. Start

```bash
skeleton --start
```

Starts the configured application services.