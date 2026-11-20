from typing import Any

from ...cmd.command import Command

from ...context.roles import Role
from ...context.context import CLIContext

from ...decorators.command import command

from ...validation.licenses import LICENSES
from ..implementations.config import config as execute_config

@command(

    roles=[Role.CLIENT],

    factory=lambda context: Command.Definition(

        name="config",
        
        description="Generate skeleton-*.json config files!",
    
        flags=["dry", "verbose"],
    
        arguments={
            
            # Profile list is dynamically
            # generated from profile folders:
    
            # "vanilla", "react", "solid", etc.
    
            # To create/register a new profile entry,
            # create a folder containing relevant boilerplate!
    
            "profile": sorted(
                context.FRAMEWORK
                .BOILERPLATE.profiles
            ),
    
            "title": "*",
            "name": "*",
            "version": "*",
            "author": "*",
            "description": "*",
            "license": LICENSES,
        },
    
        defaults={
    
            "profile": "vanilla",
    
            "title": "Skeleton Project",
            "name": "Skeleton Project",
            "version": "0.0.0",
            "author": "client",
            "description": "Skeleton + FastAPI + Webpack client project",
            "license": "MIT",
        }
    ),    
)
def config(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    return execute_config(
        values=values,
        context=context,
    )