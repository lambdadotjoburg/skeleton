from pathlib import Path

from ..repository.manifest import PackageManifest

class NodeLayout:

    root: Path

    @property
    def package(self) -> Path:
        return self.root / "package.json"

    @property
    def manifest(self) -> PackageManifest:
        return PackageManifest(path=self.package)

    @property
    def npm(self) -> str:

        import shutil
        
        # npm = "npm.cmd" if os.name == "nt" else "npm"
        # gets npm from ENV vars!
        npm = shutil.which("npm")
    
        if npm is None:
            raise FileNotFoundError(
                "npm was not found:\n"
                "Install Node.js & npm first!"
            )

        return npm