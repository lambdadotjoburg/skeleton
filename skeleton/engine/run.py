import asyncio

import sys

from .launch import launch

from ..layout.engine import EngineLayout

def run(*, engine: EngineLayout) -> int:

    print(
        "\n"
        "\t Runtime Mode: "
        f"{engine.client.mode}"
        "\n"
    )

    try:
        # Orchestrate services...
        return asyncio.run(launch(engine=engine))

    except KeyboardInterrupt:

        print(
            "\n"
            "Skeleton orchestrator interrupted!"
            "\n"
            "shutdown complete!",
            flush=True,
        )

        return 130

    except (OSError, ValueError, KeyError) as error:

        print(
            f"Orchestration failed: {error}",
            file=sys.stderr,
        )

        return 1
