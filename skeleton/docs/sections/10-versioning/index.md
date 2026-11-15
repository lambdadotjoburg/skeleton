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