from typing import Any

from .mode import RuntimeMode

class RuntimeConfig:

    RESERVED_WEBPACK_ENV = {
        "root",
        "mode",
        "host",
        "port",
    }

    def __init__(self, config: dict[str, Any]):
        self.config = config
        self._mode: RuntimeMode | None = None

    @property
    def mode(self) -> RuntimeMode:

        if self._mode is not None:
            return self._mode

        return RuntimeMode(self.config["mode"])

    @mode.setter
    def mode(self, value: RuntimeMode) -> None:
        self._mode = value

    @property
    def webpack(self) -> dict[str, Any]:

        webpack = self.config.get("webpack", {})

        if not isinstance(webpack, dict):
            raise TypeError(
                "Runtime configuration "
                "'webpack' "
                "must be an object."
            )

        env = webpack.get("env", {})
        if not isinstance(env, dict):
            raise TypeError(
                "Runtime configuration "
                "'webpack.env' "
                "must be an object."
            )

        reserved = self.RESERVED_WEBPACK_ENV.intersection(env)

        if reserved:
            keys = ", ".join(sorted(reserved))
            raise ValueError(
                "Reserved Webpack "
                "environment variables: "
                f"{keys}"
            )

        return env