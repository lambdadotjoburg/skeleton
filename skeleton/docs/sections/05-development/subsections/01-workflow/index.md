## Development Commands

Framework development commands are run from the repository root using `python run.py`.

| Command                 | Purpose                                 |
|-------------------------|-----------------------------------------|
| `python run.py --dist`  | Builds the framework distribution.      |
| `python run.py --demo`  | Creates a demo project & installs dist. |
| `python run.py --purge` | Removes framework build artifacts.      |

To specify a demo project location:

```bash
python run.py --demo --target path/to/demo/project
```

The demo operation creates the project directory,
including its `.venv` environment, and installs
the framework dist into that environment.
