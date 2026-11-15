from enum import StrEnum

class RuntimeMode(StrEnum):
    DEV = "development" # HMR + dev logs
    PROD = "production" # HMR? + test logs
    TEST = "test" # tree shaking => dist
    BUILD = "build" # tree shaking + prod logs
    PREVIEW = "preview" # run backend, gateway, + dist frontend!
