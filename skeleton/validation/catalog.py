from .validate import Rules

from .rules.dependencies import (
    npm_dependencies,
    python_dependencies,
)

DEPENDENCY_RULES: Rules = {

    "frontend": [
        npm_dependencies,
    ],

    "backend": [
        python_dependencies,
    ],
}