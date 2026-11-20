from __future__ import annotations

from pathlib import Path

from typing import Any, override

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from tomlkit import TOMLDocument

class Manifest:

    path: Path

    def update(
        self,
        supplied: dict[str, dict[str, str]],
    ) -> None:
        raise NotImplementedError

    def calculate(
        self,
        supplied: dict[str, dict[str, str]],
    ) -> dict[str, dict[str, dict[str, str]]]:

        existing = self.dependencies

        changes: dict[str, dict[str, dict[str, str]]] = {

            "added": {
                "dependencies": {},
                "devDependencies": {},
            },

            "updated": {
                "dependencies": {},
                "devDependencies": {},
            },
            
            "removed": {
                "dependencies": {},
                "devDependencies": {},
            },
        }

        for section in ("dependencies", "devDependencies"):

            current = existing[section]
            proposed = supplied[section]

            for name, version in proposed.items():

                if name not in current:
                    changes["added"][section][name] = version

                elif current[name] != version:
                    changes["updated"][section][name] = version

            for name, version in current.items():

                if name not in proposed:
                    changes["removed"][section][name] = version

        return changes

    @property
    def dependencies(
        self,
    ) -> dict[str, dict[str, str]]:
        raise NotImplementedError

    # Serialize the in-memory manifest
    def dumps(self) -> str:
        raise NotImplementedError

class PackageManifest(Manifest):

    document: dict[str, Any]

    # Load manifest from disk
    def __init__(self, path: Path):

        self.path = path

        import json

        self.document = json.loads(
            self.path.read_text(
                encoding="utf-8"
            )
        )

    @property
    def scripts(self) -> dict[str, str]:

        scripts = self.document.get("scripts", {})

        if not isinstance(scripts, dict):
            raise ValueError(
                "Invalid package.json: "
                "'scripts' must be an object."
            )

        result: dict[str, str] = {}

        for name, command in scripts.items():

            if not isinstance(name, str) or not isinstance(command, str):
                raise ValueError(
                    "Invalid package.json: "
                    "script names and commands must be strings."
                )

            result[name] = command

        return result

    @override
    def dumps(self) -> str:

        import json

        return json.dumps(
            self.document,
            indent=4,
            ensure_ascii=False,
        )

    @override
    def update(
        self,
        supplied: dict[str, dict[str, str]],
    ) -> None:

        if supplied == self.dependencies:
            return

        self.document["dependencies"] = supplied["dependencies"]
        self.document["devDependencies"] = supplied["devDependencies"]

    @override
    @property
    def dependencies(self) -> dict[str, dict[str, str]]:

        return {

            "dependencies": dict(
                self.document.get("dependencies", {})
            ),

            "devDependencies": dict(
                self.document.get("devDependencies", {})
            ),
        }

class PyProjectManifest(Manifest):

    document: TOMLDocument

    # Load manifest from disk
    def __init__(self, path: Path):

        self.path = path

        import tomlkit

        self.document = tomlkit.parse(
            self.path.read_text(
                encoding="utf-8"
            )
        )

    @override
    def dumps(self) -> str:

        import tomlkit

        return tomlkit.dumps(self.document)

    @override
    def update(
        self,
        supplied: dict[str, dict[str, str]],
    ) -> None:

        import tomlkit

        if supplied == self.dependencies:
            return

        project = self.document["project"]

        project["dependencies"] = tomlkit.array().multiline(True)

        for name, version in supplied["dependencies"].items():
            project["dependencies"].append(f"{name}{version}")

        optional_dependencies = project.setdefault(
            "optional-dependencies",
            {},
        )

        optional_dependencies["dev"] = tomlkit.array().multiline(True)

        for name, version in supplied["devDependencies"].items():
            optional_dependencies["dev"].append(f"{name}{version}")

    # TODO: v1.0.3
    # Preserve pyproject.toml syntax like:
    # 1) extras
    # 2) environment markers
    # 3) direct-reference URLs
    @override
    @property
    def dependencies(self) -> dict[str, dict[str, str]]:
        
        from packaging.utils import canonicalize_name
        from packaging.requirements import Requirement
    
        project = self.document["project"]
    
        result: dict[str, dict[str, str]] = {
            "dependencies": {},
            "devDependencies": {},
        }
    
        sections = {
            "dependencies": project.get("dependencies", []),
            "devDependencies": project
                .get("optional-dependencies", {})
                .get("dev", []),
        }
    
        for section, requirements in sections.items():
    
            for requirement in requirements:
    
                parsed = Requirement(requirement)
    
                if parsed.extras or parsed.marker or parsed.url:
                    raise ValueError(
                        "Unsupported dependency requirement: "
                        f"{requirement!r}. "
                        "Only package names and version "
                        "specifiers are currently supported!"
                    )
    
                name = canonicalize_name(parsed.name)
    
                if name in result[section]:
                    raise ValueError(
                        f"Duplicate project dependency: {name!r}"
                    )
    
                # result[section][name] = str(parsed.specifier)
                # result[section][name] = requirement[len(parsed.name):]
                result[section][name] = requirement.removeprefix(parsed.name).strip()
    
        return result

        