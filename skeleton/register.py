from .cli import *

# for access to framework resouces,
# if needed to construct special cli
# operations with internal knowledge!
from .layout.framework import FrameworkLayout

def create_registry(framework: FrameworkLayout):

    # role based command execution!
    from .context.roles import Role

    # runtime server/orcherstration mode
    from .runtime.mode import RuntimeMode

    # cmd line types!
    from .cmd.command import Command
    from .cmd.registry import CommandRegistry

    from .parsers.bump import custom_bump_parser
    from .parsers.help import custom_help_parser

    from .validation.licenses import LICENSES

    return CommandRegistry(
        [
            Command(
                
                action=vscode,

                definition=Command.Definition(
                    
                    description="Generate .vscode/settings.json config!",

                    flags=["dry", "verbose",],

                    arguments={
                        # eventually, these feature args
                        # should be dynamically obtained!
                        "feature": ["mypy", "markdown",],
                    }
                ),
            ),

            Command(

                action=help,

                parser=custom_help_parser,

                definition=Command.Definition(

                    arguments={
                        "commands": ["*"]
                    },

                    defaults={
                        "commands": []
                    },
                    
                    description="Show help for skeleton commands!",
                ),
            ),

            Command(

                action=readme,

                definition=Command.Definition(

                    arguments={
                        "write": "*",
                        "section": list(framework.DOCUMENTATION.sections),
                    },

                    defaults={
                        "write": None,
                        "section": None,
                    },

                    description="Inspect/generate Skeleton Framework docs",
                ),
            ),

            Command(

                action=tree,
                
                definition=Command.Definition(
                    
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

                        "dirs": False,
                        "files": False,
                        "hidden": False,
                        "all": False,
                        "ignored": False,
                    }
                ),
            ),

            Command(

                action=dist,

                definition=Command.Definition(

                    description="Build dist output!",

                    flags=[
                        "dry",
                        "verbose",
                        "backend",
                        "frontend"
                    ],

                    defaults={
                        "verbose": False,
                        "backend": False,
                        "frontend": False,
                    },
                ),
            ),

            Command(

                action=purge,

                definition=Command.Definition(

                    description="purge build/dist artifacts!",

                    flags=[
                        "dry",
                        "verbose",
                        "frontend",
                        "backend",
                    ],

                    defaults={
                        "verbose": False,
                        "backend": False,
                        "frontend": False,
                    },
                ),
            ),

            Command(

                action=config,

                roles=[Role.CLIENT],
                
                definition=Command.Definition(
                    
                    description="Generate skeleton-*.json config files!",

                    flags=["dry", "verbose"],

                    arguments={
                        
                        # Profile list is dynamically
                        # generated from profile folders:

                        # "vanilla", "react", "solid", etc.

                        # To create/register a new profile entry,
                        # create a folder containing relevant boilerplate!

                        "profile": sorted(framework.BOILERPLATE.profiles),

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
            ),

            Command(
                
                action=init,

                roles=[Role.CLIENT],

                definition=Command.Definition(
                    
                    description="initialize & prepare app!",
                    
                    flags=[

                        "dry",
                        "verbose",

                        "backend",
                        "frontend"
                    ],

                    defaults={
                        "verbose": False,
                        "backend": False,
                        "frontend": False,
                    }
                ),
            ),

            Command(
                
                action=install,

                roles=[Role.CLIENT],

                definition=Command.Definition(
                    
                    description="install app dependencies!",

                    flags=[

                        "dry",
                        "verbose",
                        
                        "backend",
                        "frontend",

                        "editable"
                    ],
                    
                    defaults={
                        "verbose": False,
                        "backend": False,
                        "frontend": False,
                        "editable": True,
                    }
                ),
            ),

            Command(

                action=start,

                roles=[Role.CLIENT],
                
                definition=Command.Definition(
                    
                    description=(
                        "start skeleton orchestration "
                        "engine & launch gateway server!"
                    ),

                    arguments={

                        "mode": [
                            mode.value
                            for mode in RuntimeMode
                        ],
                        
                        # maybe allow client to
                        # explicitly override gateway
                        # port + host

                        # "port": ["8000"],
                        # "host": ["127.0.0.1"],
                    },

                    defaults={
                        
                        "mode": None,

                        # maybe allow client to
                        # explicitly override gateway
                        # port + host

                        # "port": "8000",
                        # "host": "127.0.0.1",
                    },
                ),
            ),

            Command(
                
                action=preview,
                roles=[Role.CLIENT],
                
                definition=Command.Definition(
                    
                    description=(
                        "preview frontend build app!"
                    ),

                    arguments={
                        "mode": [RuntimeMode.PREVIEW.value],
                    },

                    defaults={
                        "mode": RuntimeMode.PREVIEW.value,
                    },
                ),
            ),

            Command(

                action=bump,

                parser=custom_bump_parser,
                
                definition=Command.Definition(
                    
                    description=(
                        "Update release version: "
                        "major, minor, patch!"
                    ),

                    arguments={
                        "major": "*", # number/bool
                        "minor": "*", # number/bool
                        "patch": "*", # number/bool
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

                        "sync": False,
                        "backend": False,
                        "frontend": False,
                        
                        "major": False,
                        "minor": False,
                        "patch": False,
                    },
                ),
            ),

            Command(
                        
                action=demo,

                roles=[Role.FRAMEWORK],

                definition=Command.Definition(
                    
                    description=(
                        "Install client project from local dist!"
                    ),

                    flags=[
                        "dry",
                        "verbose",
                    ],

                    arguments={
                        "target": "*"
                    },

                    defaults={
                        "target": "./demo"
                    },
                ),
            ),

            Command(

                action=quickstart,

                roles=[Role.CLIENT],

                definition=Command.Definition(
                    
                    description=(
                        "quick start an application, "
                        "--config + --init + --install"
                    ),

                    flags=[
                        "dry",
                        "verbose",
                    ],

                    arguments={
                        "profile": sorted(framework.BOILERPLATE.profiles),
                    },

                    defaults={
                        "profile": "vanilla",
                    },
                ),
            ),

            # Command(
            
            #     action=monitor,
                
            #     definition=Command.Definition(
                    
            #         description=(
            #             "Monitor running python processes!"
            #         ),

            #         flags=[ "once" ],

            #         arguments={
                        
            #             "scope": [

            #                 "framework",
            #                 "client",
            #                 "all",
            #             ],

            #             "filter": [
                            
            #                 "npm",
            #                 "node",
            #                 "webpack",

            #                 "python",
            #                 "uvicorn",
            #             ],
            #         },

            #         defaults= {
                        
            #             "scope": "all",

            #             "filter": [
            #                 "npm",
            #                 "node",
            #                 "webpack",

            #                 "python",
            #                 "uvicorn",
            #             ]
            #         },
            #     ),
            # ),
        ],
    )