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