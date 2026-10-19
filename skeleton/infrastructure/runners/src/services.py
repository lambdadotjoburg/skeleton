from skeleton.infrastructure.runners.src import (
    packages
)
from skeleton.infrastructure.runners.src import frontend, gateway

# let tsc handle packages build-order
SERVICES = {
    "packages": packages,
    "frontend": frontend,
    "gateway": gateway,
}

DEFAULT_TARGETS = [
    "frontend",
    "gateway",
]
