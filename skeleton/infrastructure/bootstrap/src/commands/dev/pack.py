import os, shutil
import subprocess

from pathlib import Path

def dev_pack(framework_root: Path) -> None:

    framework_root = framework_root.resolve()

    packages_root = framework_root / "skeleton" / "packages"
    artifacts_root = packages_root / ".skeleton"

    npm = "npm.cmd" if os.name == "nt" else "npm"

    # 1. Build both packages from the framework root.
    subprocess.run(
        [npm, "run", "packages:build"],
        cwd=framework_root,
        check=True,
    )

    # 2. Recreate the predictable output directory.
    if artifacts_root.exists():
        
        shutil.rmtree(artifacts_root)

    artifacts_root.mkdir(parents=True)

    # 3. Pack webpack first, then the CLI.
    for name in ("webpack", "cli"):

        package_root = packages_root / name

        if not (package_root / "package.json").is_file():

            raise FileNotFoundError(
                f"Package manifest not found: "
                f"{package_root / 'package.json'}"
            )

        subprocess.run(
            [
                npm,
                "pack",
                "--pack-destination",
                str(artifacts_root),
            ],
            cwd=package_root,
            check=True,
        )

    print(
        f"\nSkeleton packages created in:\n"
        f"{artifacts_root}"
    )
