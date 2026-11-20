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