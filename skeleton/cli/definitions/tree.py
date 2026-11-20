from typing import Any

from ...context.roles import Role
from ...context.context import CLIContext
from ...decorators.command import command

from ..implementations.tree import tree as execute_tree

@command(
    
    name="tree",

    roles=[Role.CLIENT, Role.FRAMEWORK],

    description="Directory-tree operation!",
                        
    arguments={
        "dir": "*", # dir to traverse
        "depth": "*", # integer/number
        "exclude": ["*"], # pattern
    },

    flags=[
        "dirs",
        "files",
        "hidden",
        "all",
        "ignored",
    ],
    
    defaults={

        "dir": ".", # dir to traverse
        "depth": "1", # integer/number
        "exclude": [], # pattern
    }
)
def tree(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_tree(
        values=values,
        context=context,
    )