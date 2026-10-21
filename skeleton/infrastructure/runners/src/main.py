from pathlib import Path

from skeleton.infrastructure.runners.src.cmd import CMD
from skeleton.infrastructure.runners.src.process import ProcessManager

from skeleton.infrastructure.common.src.constants import Bootstrap
from skeleton.infrastructure.common.src.context import RuntimeContext

from skeleton.infrastructure.common.src.config import load_runtime_config
from skeleton.infrastructure.common.src.layout import build_layout
from skeleton.infrastructure.common.src.env import build_env

from skeleton.infrastructure.runners.src.parser import parse

from skeleton.infrastructure.runners.src.services import SERVICES
from skeleton.infrastructure.runners.src.services import DEFAULT_TARGETS

def run(
    framework_root: Path,
    project_root: Path,
    argv: list[str],
):

    raw = parse(argv)

    raw["options"]["root"] = str(project_root)

    if not raw["targets"]:
        raw["targets"] = list(DEFAULT_TARGETS.copy())

    cmd = CMD(**raw)

    MODE = str(cmd.options.get("mode", "dev"))

    env = build_env(project_root, MODE)

    layout = build_layout(
        project_root / Bootstrap.LAYOUT,
        project_root=project_root,
        framework_root=framework_root,
    )

    config = load_runtime_config(
        layout.common / Bootstrap.CONFIG_FILE_EXT,
        project_root,
        framework_root,
        # layout,
    )

    context = RuntimeContext(
        root=project_root,
        mode=MODE,
        args=argv,
        env=env,
        layout=layout,
        config=config,
        options=cmd.options,
    )

    manager = ProcessManager(context)

    if context.options.get("open") and context.mode == "dev":

        from skeleton.infrastructure.runners.src.hook import (
            create_dev_portal
        )

        manager.register_hook(
            create_dev_portal(context),
            "after_start"
        )

    for target in cmd.targets:
        service = SERVICES[target]
        handler = getattr(service, cmd.action)
        manager.register(handler(context))

    manager.start()