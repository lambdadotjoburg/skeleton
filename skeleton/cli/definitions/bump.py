from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ...parsers.bump import custom_bump_parser

from ..implementations.bump import bump as execute_bump

@command(
    
    name="bump",

    description=(
        "Update release version: "
        "major, minor, patch!"
    ),

    parser=custom_bump_parser,

    roles=[Role.CLIENT, Role.FRAMEWORK],

    arguments={
        "major": "*",
        "minor": "*",
        "patch": "*",
    },

    flags=[
        "dry",
        "verbose",
        "sync",
        "backend",
        "frontend",
        "force",
    ],

    defaults={
        "major": False,
        "minor": False,
        "patch": False,

        # "dry": False,
        # "verbose": False,
        "backend": False,
        "frontend": False,
    },
)
def bump_command(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_bump(
        values=values,
        context=context,
    )