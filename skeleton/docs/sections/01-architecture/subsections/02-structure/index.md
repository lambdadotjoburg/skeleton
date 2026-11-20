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