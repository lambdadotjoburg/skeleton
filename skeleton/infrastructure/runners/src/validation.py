from skeleton.infrastructure.runners.src.cmd import CMD
from skeleton.infrastructure.runners.src.actions import ACTIONS
from skeleton.infrastructure.runners.src.services import SERVICES

class CMDValidationError(Exception):
    pass

def validate(cmd: CMD):

    if cmd.action not in ACTIONS.values():
        raise CMDValidationError(
            f"Unknown action: {cmd.action}"
        )

    for target in cmd.targets:
        
        if target not in SERVICES:
            raise CMDValidationError(
                f"Unknown service: {target}"
            )

        service = SERVICES[target]

        if not hasattr(service, cmd.action):
            raise CMDValidationError(
                f"Service {service}" f" "
                f"does not have action {cmd.action}"
            )