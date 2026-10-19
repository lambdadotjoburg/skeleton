import logging
import uvicorn

from copy import deepcopy

class AccessLogFilter(logging.Filter):

    def filter(
        self,
        record: logging.LogRecord
    ) -> bool:

        return (
            "GET /.well-known/appspecific/com.chrome.devtools.json "
            not in record.getMessage()
        )

def build_log_config() -> dict:

    config = deepcopy(
        uvicorn.config.LOGGING_CONFIG
    )

    config["filters"] = {
        "skeleton_access": {
            "()": (
                "skeleton.infrastructure.gateway.src.logging."
                "AccessLogFilter"
            ),
        },
    }

    config["handlers"]["access"]["filters"] = [
        "skeleton_access",
    ]

    return config