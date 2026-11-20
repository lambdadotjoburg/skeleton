## Maintenance

To manage generated project dist, build artifact and outputs, skeleton provides lifecycle commands:

| Command            | Purpose                                     |
|--------------------|---------------------------------------------|
| `skeleton --dist`  | Builds the client distribution.             |
| `skeleton --purge` | Removes generated build artifacts.          |

**CAUTION**

`--purge` is destructive & will remove all build artifacts
as listed in `config/skeleton-project.json`, including `node_modules`.