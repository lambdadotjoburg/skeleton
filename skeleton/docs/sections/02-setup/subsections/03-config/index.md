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