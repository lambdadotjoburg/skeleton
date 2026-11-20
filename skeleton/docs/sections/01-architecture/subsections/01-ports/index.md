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