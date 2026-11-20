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