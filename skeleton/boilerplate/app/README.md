# {{ title }}

## {{ name }}

**Version:** {{ version }}

{{ description }}

## Project Information

| Property | Value |
|---|---|
| Profile | {{ profile }} |
| Title | {{ title }} |
| Name | {{ name }} |
| Version | {{ version }} |
| Author | {{ author }} |
| Created | {{ date }} |

## Project Structure

This project is organised into two main components: a frontend application and a backend API.

### Frontend

The frontend provides the application's user interface, built using **{{ profile }}**.

- **Location:** `{{ frontend }}`
- **Project name:** {{ name }}
- **Version:** {{ version }}

Frontend dependencies and development dependencies are managed through `{{ frontend }}/package.json`.

### Backend

The backend provides the application's API, powered by **FastAPI**.

- **Location:** `{{ backend }}`
- **Distribution name:** {{ name }}
- **Application:** `{{ app }}`
- **Python environment:** `{{ venv }}`
- **Python interpreter:** `{{ venv_python }}`

Backend dependencies and development dependencies are managed through `{{ backend }}/pyproject.toml`.

## Getting Started

### Requirements

Before getting started, ensure that you have:

- Python 3.11 or later
- Node.js and npm
- Skeleton Framework installed and available on your PATH

## Help

To find help for all available commands, do:

```bash
skeleton --help
```

It might also be useful to inspect the project tree:

```bash
skeleton --tree --depth 5
```

## Configuration

Project configuration is stored in the `config/` directory.

The configuration files control project metadata, frontend profiles, dependencies, server settings, proxy behaviour, and application setup.

To generate or update the project configuration, run:

```bash
skeleton --config --profile {{ profile }}
```

To initialise the project structure, run:

```bash
skeleton --init
```

### Installation

From the project root, run:

```bash
skeleton --install
```

This installs the frontend and backend dependencies using their respective package managers.

### Running the Application

Start the application with:

```bash
skeleton --start
```

## Further Information

For further information about Skeleton Framework, visit the [Skeleton Framework GitHub repository](https://github.com/lambdadotjoburg/skeleton).