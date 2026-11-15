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