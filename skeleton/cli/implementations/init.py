import json

from typing import Any

from datetime import datetime

from ...decorators.roles import roles

from ...context.roles import Role
from ...context.context import CLIContext

@roles(Role.CLIENT)
def init(
    *,
    values: dict[str, Any],
    context: CLIContext,
) -> int:

    layout = context.CLIENT

    if layout is None:
        raise RuntimeError("Client layout is unavailable.")

    boilerplate = context.FRAMEWORK.BOILERPLATE

    dry = values.get("dry", False) is True
    verbose = values.get("verbose", False) is True
    
    backend = values.get("backend", False) is True
    frontend = values.get("frontend", False) is True

    if not backend and not frontend:
        backend = True
        frontend = True

    try:
        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        try:
            layout.config.require(
                [
                    "skeleton-dependencies.json",
                    "skeleton-metadata.json",
                    "skeleton-project.json",
                    "skeleton-schemas.json",
                ]
            )
        except FileNotFoundError as error:
            print(error)
            return 1

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        # define local variables

        metadata = layout.config.load("skeleton-metadata.json")
        schemas = layout.config.load("skeleton-schemas.json")
        api = schemas["http"]["backend"]["prefix"].strip("/")
        # ws = schemas["ws"]["backend"]["prefix"].strip("/")

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        # validate profile choice!

        from ...validation.rules.choice import choice
        from ...validation.validate import validate
        from ...validation.metadata import INIT_RULES

        profile_rules = {
            "profile": [
                *INIT_RULES["profile"],
                choice(boilerplate.profiles),
            ],
        }

        profile_errors = validate(
            values=metadata,
            rules=profile_rules,
        )

        if profile_errors:
            for e in profile_errors:
                print(e)
            return 1

        profile = boilerplate.profile(metadata["profile"])

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        from ...template.normalize import snake

        variables = {

            **metadata,

            "_normalized_name": snake(metadata["name"]),

            "frontend": layout.frontend.dir,
            "backend": layout.backend.dir,

            "api": api,

            "app": layout.backend.app,
            
            "venv": layout.backend
                .venv.relative_to(
                    layout.backend.root
                ).as_posix(),

            "venv_python": layout.backend
                .venv_python.relative_to(
                    layout.backend.root
                ).as_posix(),

            "year": str(datetime.now().year),
        }

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#
        
        # validate the client's config value!

        errors = validate(
            values=variables,
            rules=INIT_RULES,
        )

        if errors:
            for e in errors:
                print(e)
            return 1

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#
        
        # validate dependencies!

        from ...validation.catalog import DEPENDENCY_RULES

        dependencies = layout.dependencies

        dependency_rules = {}

        if frontend:
            dependency_rules["frontend"] = DEPENDENCY_RULES["frontend"]

        if backend:
            dependency_rules["backend"] = DEPENDENCY_RULES["backend"]

        errors = validate(
            values=dependencies,
            rules=dependency_rules,
        )

        if errors:
            for e in errors:
                print(e)
            return 1

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        from ...template.render import render

        # client/README.md
        readme = render(
            boilerplate.app.readme
            .read_text(encoding="utf-8"),
            variables=variables
        )

        # client/LICENSE.md
        license = render(
            boilerplate.app.license
            .read_text(encoding="utf-8"),
            variables=variables
        )

        if frontend:
    
            # client/frontend/src/index.html
            index = render(
                boilerplate.app.index
                .read_text(encoding="utf-8"),
                variables=variables,
            )

            from ...repository.reconcile import reconcile

            manifest = boilerplate.app.manifest("frontend")

            updated = reconcile(
                existing=manifest.dependencies,
                configured=dependencies.get("frontend", {}),
                remove=False,
            )

            manifest.update(updated)

            package = render(
                manifest.dumps(),
                variables=variables,
            )

        if backend:

            # client/backend/src/main.py
            main = render(
                boilerplate.app.main
                .read_text(encoding="utf-8"),
                variables=variables
            )

            from ...repository.reconcile import reconcile

            manifest = boilerplate.app.manifest("backend")

            updated = reconcile(
                existing=manifest.dependencies,
                configured=dependencies.get("backend", {}),
                remove=False,
            )

            manifest.update(updated)

            # client/backend/pyproject.toml
            pyproject = render(
                manifest.dumps(),
                variables=variables,
            )

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        # construct project plan!

        from ...template.plan import ProjectPlan
        from ...template.asset import Asset, Template

        files=[

            # source => target
            Asset(
                source=boilerplate.app.gitignore,
                destination=layout.gitignore,
            )
        ]

        folders=[

            Asset(
                source=boilerplate.PLUGINS,
                destination=layout.plugins
            )
        ]

        if backend:

            folders.extend(
                [
                    Asset(
                        source=boilerplate.app.backend,
                        destination=layout.backend.root,
                    ),
                ]
            )

        if frontend:

            folders.extend(
                [
                    # Frontend
                    Asset(
                        source=boilerplate.app.frontend,
                        destination=layout.frontend.root,
                    ),
            
                    # Profile
                    Asset(
                        source=profile.frontend,
                        destination=layout.frontend.root,
                    ),
                ]
            )

        templates=[

            Template(
                source=boilerplate.app.readme,
                destination=layout.readme,
                content=readme,
            ),

            Template(
                source=boilerplate.app.license,
                destination=layout.license,
                content=license,
            ),
        ]

        if frontend:

            templates.extend(
                [
                    # frontend templates/assets
                    Template(
                        source=boilerplate.app.index, # ignore source
                        destination=layout.frontend.index,
                        content=index,
                    ),
        
                    Template(
                        source=boilerplate.app.package, # ignore source
                        destination=layout.frontend.package,
                        content=package,
                    ),
                ]
            )

        if backend:

            templates.extend(
                [
                    # backend templates/assets
                    Template(
                        source=boilerplate.app.main, # ignore source
                        destination=layout.backend.main,
                        content=main,
                    ),
        
                    Template(
                        source=boilerplate.app.pyproject, # ignore source
                        destination=layout.backend.pyproject,
                        content=pyproject,
                    ),
                ]
            )

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        # construct the client's project plan!
        
        plan = ProjectPlan(
            root=layout.root,
            files=files,
            folders=folders,
            templates=templates,
        )

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

        from ...template.generate import generate

        # create the client's actual project!
        generate(plan, verbose=verbose, dry=dry)

        if backend:
            
            # create backend .venv!
            environment = layout.backend.venv
            
            if not environment.exists():

                if dry:
                    print(f"Virtual environment will be created: {environment}")
                else:

                    if verbose:
                        print(f"Creating virtual environment: {environment}")

                    from ...environment.upgrade import upgrade
                    from ...environment.venv import create_venv

                    create_venv(target=environment)

                    result = upgrade(
                        python=layout.backend.venv_python,
                        cwd=layout.backend.root,
                        verbose=verbose,
                    )

                    if result != 0:
                        return 1

        if dry:
            print("\nDRY RUN: No modifications during project init!")
        else:
            print("\nInit complete!")
            print("Run skeleton --install")

        return 0

        #%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%*%#

    except (
        OSError,
        KeyError,
        ValueError,
    ) as error:

        print(
            "Failed to inspect "
            "project initialization: "
            f"{error}"
        )

        return 1
    