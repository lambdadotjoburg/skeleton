# Skeleton Framework

![Skeleton Logo](https://raw.githubusercontent.com/lambdadotjoburg/skeleton/main/skeleton.png)

## Overview

Skeleton is a full-stack application orchestration framework
that combines Python orchestration, a FastAPI reverse-proxy gateway,
a Python backend, and a TypeScript frontend.

It provides a structured development workflow for configuring,
initializing, installing, running, and building full-stack applications.

Skeleton supports multiple frontend profiles and manages the development
environments and tooling required by each application component.

## Features

- **Python orchestration** for project configuration, initialization, dependency installation and service execution.
- **FastAPI gateway** for centralizing request routing and communication with backend services.
- **Python backend** for application APIs.
- **Multiple frontend profiles** supports Vanilla TypeScript, React, SolidJS, Vue, and Svelte.
- **Webpack tooling** for frontend development and production builds.
- **JSON-based configuration** for project metadata, structure, dependencies, schemas, servers, etc.
- **Command-line interface** for project management, development, versioning, distribution, and cleanup.
- **Plugins & Extension Points** for extending skeleton framework internals like custom commands and scripts.

# Architecture

Skeleton employs a modular, layered architecture
to separate project orchestration, gateway services,
backend APIs, and frontend tooling.

## Layers

Skeleton separates the application into cooperating layers:

| Layer                     | Technology  |
|---------------------------|-------------|
| Orchestration and CLI     | Python      |
| Gateway                   | FastAPI     |
| Backend APIs              | FastAPI     |
| HTTP server               | Uvicorn     |
| HTTP communication        | HTTPX       |
| Frontend                  | TypeScript  |
| Frontend bundling         | Webpack     |
| Development file watching | watchfiles  |
| Dependency management     | pip and npm |

The gateway provides a central entry point for browser requests
and coordinates communication between the frontend and backend.

## Default Ports

The default development configuration uses the following ports:

| Service                     | Address               |
|-----------------------------|-----------------------|
| Gateway / reverse proxy     | http://127.0.0.1:8000 |
| Backend API                 | http://127.0.0.1:8080 |
| Frontend development server | http://127.0.0.1:3000 |

The gateway is the normal entry point for browser access.

For example, the index API endpoint can be accessed through:

```text
http://127.0.0.1:8000/api/
```

The corresponding backend endpoint may be available directly at:

```text
http://127.0.0.1:8080/
```

Actual routes depend on the application's server and gateway configuration.

## Client Project Structure

A client project consists of three main directories:

- `config/` - project and service configuration files.
- `backend/` - Python application and API.
- `frontend/` - TypeScript application and static assets.

The project root also contains its `README.md` and `.gitignore` files.

Dependency installation creates a backend `.venv/` and frontend `node_modules/` directory.

The exact structure depends on the selected frontend profile and project configuration.

Optional VS Code settings are generated in `.vscode/`.

To generate the optional `.vscode` settings for mypy support, run:

```bash
skeleton --vscode --feature mypy
```

To generate the optional `.vscode` settings for markdown support, run:

```bash
skeleton --vscode --feature markdown
```

# Project Setup

Skeleton Framework is distributed through [PyPI](https://pypi.org/project/skeleton-framework/)
and its source code is hosted on [GitHub](https://github.com/lambdadotjoburg/skeleton).

This section covers installing Skeleton, creating a project, and configuring its environment.

## Installation

### 1. Requirements

Before getting started, install:

- Python 3.11 or later & pip.
- Node.js & npm.

### 2. .venv

It is recommended to create and activate a Python virtual environment before installing Skeleton.

From your project directory, run:

```bash
python -m venv .my-venv
```

Activate the environment using the command for your shell:

**Windows CMD**

```bat
.my-venv\Scripts\activate.bat
```

**Windows PowerShell**

```powershell
.\.my-venv\Scripts\Activate.ps1
```

**Git Bash**

```bash
source .my-venv/Scripts/activate
```

On **macOS / Linux** do:

```bash
source .my-venv/bin/activate
```

### 3. pip installation

Install Skeleton from PyPI:

```bash
python -m pip install skeleton-framework
```

The installed Python distribution provides the `skeleton` command.

## Quickstart

Create or enter an empty directory for your application:

```bash
mkdir my-app
cd my-app
```

Use the `quickstart` operation to configure & initialize
a client project & install its dependencies, for example:

```bash
skeleton --quickstart --profile solid
```

The frontend profile is optional.

If omitted, Skeleton uses the default Vanilla TypeScript profile:

```bash
skeleton --quickstart
```

To run the application:

```bash
skeleton --start
```

Follow the terminal output for service startup information
and open the application at the configured local address.

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

## Configuration

Skeleton stores project configuration in the `config/` directory.
Configuration files use the `skeleton-*.json` naming convention.

| File                         | Purpose                                                |
|------------------------------|--------------------------------------------------------|
| `skeleton-metadata.json`     | Project metadata and frontend profile.                 |
| `skeleton-project.json`      | Project directories, paths, and build settings.        |
| `skeleton-dependencies.json` | Authoritative frontend and backend dependencies.       |
| `skeleton-servers.json`      | Gateway, frontend, and backend host and port settings. |
| `skeleton-schemas.json`      | HTTP and WebSocket gateway routing rules.              |
| `skeleton-fastapi.json`      | Backend reload settings.                               |
| `skeleton-portal.json`       | Browser launch and API documentation settings.         |
| `skeleton-webpack.json`      | Frontend Webpack configuration.                        |

## Dependencies

The `skeleton-dependencies.json` file is the authoritative source for project dependencies.

Skeleton reconciles dependencies with frontend `package.json` and backend `pyproject.toml` manifests.

Changes made directly to those manifests may be overwritten during reconciliation if not reflected in the configuration file.

Review this file before changing project dependencies.

# Command Line Interface

Skeleton provides commands for managing the client project lifecycle,
from initial configuration and dependency installation to running and building the application.

This section covers the available CLI commands, plugins, and client-defined scripts.

## Command-Line Interface

### Help

Display available commands:

```bash
skeleton --help
```

Display help for a specific command:

```bash
skeleton --help --<command>
```

### Project inspection

Inspect the project directory structure:

```bash
skeleton --tree
```

Control the displayed depth:

```bash
skeleton --tree --depth 5
```

Inspect Skeleton documentation:

```bash
skeleton --readme
```

Display a specific documentation section:

```bash
skeleton --readme --section architecture
```

Write documentation to a file/output:

```bash
skeleton --readme --write README.md
```

Or write a documentation section to a file/output:
```bash
skeleton --readme --section architecture --write ARCHITECTURE.md
```

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

# Lifecycle

Skeleton provides commands for maintaining client projects
and managing their versions throughout the application lifecycle.

## Maintenance

To manage generated project dist, build artifact and outputs, skeleton provides lifecycle commands:

| Command            | Purpose                                     |
|--------------------|---------------------------------------------|
| `skeleton --dist`  | Builds the client distribution.             |
| `skeleton --purge` | Removes generated build artifacts.          |

**CAUTION**

`--purge` is destructive & will remove all build artifacts
as listed in `config/skeleton-project.json`, including `node_modules`.

## Versioning

Use `--bump` to update the project version using semantic versioning.

The `--major`, `--minor`, and `--patch` options accept an optional integer.

If omitted, the selected component increments by one.

```bash
skeleton --bump --major
skeleton --bump --minor 4
skeleton --bump --patch 2
```

Version components follow these rules:

- **Major:** Updates the major component, resets minor & patch to zero.
- **Minor:** Updates the minor component, resets patch to zero.
- **Patch:** Updates only the patch component.

Negative values decrement the selected component,
provided the result remains positive.

Otherwise, that component is set to zero.
Version components never become negative.

For example:

```bash
skeleton --bump --patch -2
```

Decrements the patch component by two,
or sets it to zero if the result would be zero or negative.

Use `--dry` to preview the proposed version without modifying `pyproject.toml`:

```bash
skeleton --bump --patch --dry
```

Add `--verbose` for additional execution information:

```bash
skeleton --bump --patch --dry --verbose
```

The operation updates the relevant files:
- the framework's `pyproject.toml` in framework development mode
- the backend's `pyproject.toml` + `package.json` in a client project.

# Development

This section covers working on the Skeleton Framework itself,
including repository setup, development operations,
and publishing framework distributions.

## Repository Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/lambdadotjoburg/skeleton.git
cd skeleton
```

Follow the [Installation](#installation) instructions
to create and activate a virtual environment.

Install the framework in editable mode with development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Editable installation allows framework source
changes to take effect without reinstalling the package.

## Development Commands

Framework development commands are run from the repository root using `python run.py`.

| Command                 | Purpose                                 |
|-------------------------|-----------------------------------------|
| `python run.py --dist`  | Builds the framework distribution.      |
| `python run.py --demo`  | Creates a demo project & installs dist. |
| `python run.py --purge` | Removes framework build artifacts.      |

To specify a demo project location:

```bash
python run.py --demo --target path/to/demo/project
```

The demo operation creates the project directory,
including its `.venv` environment, and installs
the framework dist into that environment.

## Publish

Install or update Twine & validate the generated artifacts:

```bash
python -m pip install --upgrade twine
python -m twine check dist/*
```

Upload the distribution to TestPyPI first:

```bash
python -m twine upload --repository testpypi dist/*
```

After verifying the TestPyPI installation, upload the **same artifacts** to PyPI:

```bash
python -m twine upload dist/*
```

Use the appropriate API token when prompted. TestPyPI and PyPI require separate credentials.

Never commit API tokens or other publishing credentials to the repository.

Do not rebuild or modify the distribution between the TestPyPI and PyPI uploads.

## Project Status

Skeleton is an experimental framework under active development.

Its goal is to provide a clear, reproducible foundation for full-stack
application development while keeping configuration, orchestration,
frontend tooling, and backend services independently manageable.

## TODO

### 1. Operational Improvements

- [ ] Make skeleton tolerant of absent backend and/or frontend configuration.
- [ ] Introduce cli syntax `--stack react+node` so client can choose a combo.
- [ ] Explore combining `--dist` and `--preview` into a single operation.

### 2. Gateway Server updates

- [ ] Implement WebSocket support in the reverse-proxy gateway.

### 3. Release Validation

- [ ] Build and install the framework distribution in a demo project.
- [ ] Test the installed distribution using the standard client workflow.
- [ ] Perform integration testing before publishing releases through Hatch/Twine.

## Licence

Skeleton Framework is proprietary software. Copyright © 2026 lambdadotjoburg.
All rights reserved.

The source code is publicly available for inspection, but public availability
does not grant unrestricted rights to use, modify, or redistribute the framework.

Personal learning, educational activities, and non-commercial experimentation
are permitted under the terms of the root [LICENSE](./LICENSE) file.

Commercial use requires a separate paid licence from the copyright holder.
Redistribution requires prior written permission.

Third-party dependencies remain subject to their respective licences.

For commercial licensing, redistribution requests, or other permissions,
contact [lambdadotjoburg@gmail.com](mailto:lambdadotjoburg@gmail.com).

See the [LICENSE](./LICENSE) file for the complete terms.
