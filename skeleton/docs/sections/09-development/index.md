## Framework Development

### Installation & Setup

Clone the repository and enter its directory:

```bash
git clone https://github.com/lambdadotjoburg/skeleton.git
cd skeleton
```

Follow the [Installation](#installation) instructions
to create and activate a virtual environment.

Install the framework in editable mode with development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Editable installation allows framework source
changes to take effect without reinstalling the package.

### Development Commands

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
