# Skeleton Framework: Release and Publishing Guide

This document describes the release workflow for the Skeleton Framework source repository. The goal is to test the built Python distribution outside the source tree before publishing it to PyPI.

## Release strategy

Use this order:

1. **Publish the source repository to GitHub first.** Commit the release-ready source, README, license, packaging configuration, and this guide. GitHub becomes the canonical source of truth.
2. **Build and validate the distribution locally.**
3. **Upload the release to TestPyPI** and test installation in a clean project and virtual environment.
4. **Tag the verified source revision and create a GitHub release** if you have not already done so.
5. **Upload the same verified distribution artifacts to PyPI.**
6. **Verify installation from real PyPI.**

TestPyPI and PyPI are separate indexes. TestPyPI is for rehearsal; a successful TestPyPI installation is a release gate, not a substitute for testing the actual published PyPI package.

## 1. Confirm release metadata

Before the first release, review `pyproject.toml` and confirm:

- Distribution name: `skeleton-framework`.
- Version: `0.1.0`, provided this version has not already been published.
- Python import package remains `skeleton`.
- CLI entry point remains `skeleton = "skeleton.cli:main"`.
- Runtime dependencies are declared in `[project].dependencies`.
- The README, license, and package-data configuration are correct.
- The wheel includes the framework templates, configuration files, and bundled Node tooling archives.

The PyPI distribution name and Python import name are different concepts: users install `skeleton-framework`, but import paths and the command-line entry point can still use `skeleton`.

Check that `skeleton-framework` is available on PyPI before the first production upload. An attempted upload is the definitive availability check, but confirm the project page and name before preparing the release.

## 2. Decide the Node tooling versions

The bundled Node packages currently have their own versions, independent of the Python distribution version. They do not have to match `skeleton-framework`.

Because the Node packages are intended to be bundled inside the Python distribution rather than published independently to npm, their version numbers are internal package metadata. For a first experimental release, changing both packages from `1.0.0` to `0.1.0` is reasonable if `1.0.0` was only a placeholder and you do not consider their interfaces stable.

Before changing them, update and verify every related version reference, including the CLI package's dependency on the webpack package and any generated tarball filenames. Rebuild the archives and Python distribution after changing versions. Do not change versions merely for cosmetic consistency if `1.0.0` already reflects an intentional, stable internal tooling release.

## 3. Commit the release source to GitHub

Before publishing packages, push the release-ready source to a GitHub repository. Check that it contains at least:

- `pyproject.toml`
- `README.md` and the image it references
- A `LICENSE` file and an appropriate license declaration
- Framework source and required templates
- The release instructions in `PUBLISHING.md`

Ensure that build artifacts, virtual environments, credentials, API tokens, and local test-project files are not committed.

Run the release workflow from a clean, committed working tree. Record the commit that is being released so the tested artifacts can be traced back to that source revision.

## 4. Build the distribution

From the framework repository root, run:

```bash
python run.py --clean
python run.py --dist
```

`--dist` combines the framework's packaging and Python distribution build steps (`--pack` and `--build`). The resulting wheel and source distribution should be in `dist/`.

Check the generated artifacts:

```bash
python -m pip install --upgrade build twine
python -m twine check dist/*
```

Inspect the wheel to verify that it contains the CLI, infrastructure files, templates, configuration files, and bundled `.tgz` archives. Do not upload artifacts until these checks pass.

## 5. Upload to TestPyPI

Create an account and API token on [TestPyPI](https://test.pypi.org/). Keep the token secret; do not place it in source files or commit it to Git.

Upload the distribution artifacts:

```bash
python -m twine upload --repository testpypi dist/*
```

When prompted, authenticate using the TestPyPI credentials or an API token. TestPyPI credentials and tokens are separate from PyPI credentials and tokens.

## 6. Test the TestPyPI installation outside the framework repository

Create a sibling project directory from the framework repository root:

```bash
mkdir -p ../skeleton-test-project
cd ../skeleton-test-project
```

Create and activate a dedicated environment.

Git Bash on Windows:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

macOS or Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install Skeleton from TestPyPI while allowing its dependencies to be resolved from PyPI:

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ skeleton-framework
```

Verify the installed distribution:

```bash
python -m pip show skeleton-framework
python -m pip show -f skeleton-framework
```

Then run the end-to-end client workflow from the test project root:

```bash
skeleton --quickstart
skeleton --start
```

Check that the gateway, backend, and frontend start; that the configured routes work; and that the installed distribution can find its templates and bundled tooling without reading from the framework source checkout.

If you need to test a local wheel before uploading it, install the wheel into the same kind of clean external environment:

```bash
python -m pip install --force-reinstall ../framework/dist/skeleton_framework-0.1.0-py3-none-any.whl
```

Adjust the relative path, filename, and version to match the actual checkout and generated wheel. Do not use `--no-deps` for the initial installation unless you have already installed all declared dependencies in that environment.

## 7. Create the release tag

Once the source and TestPyPI test are satisfactory, tag the exact source commit used to produce the tested artifacts. For example:

```bash
git tag v0.1.0
git push origin v0.1.0
```

Create a GitHub release for that tag if desired, including concise release notes. If you prefer to create the tag and GitHub release before TestPyPI, that is also workable; the important requirement is that the tag identifies the exact source revision tested and released.

## 8. Publish to PyPI

Create or configure a PyPI account and API token at [PyPI](https://pypi.org/). Use a PyPI token for the production upload, not the TestPyPI token.

Upload the same, already-verified artifacts that were uploaded to TestPyPI:

```bash
python -m twine upload dist/*
```

Do not rebuild or modify the artifacts between the TestPyPI and PyPI uploads. PyPI does not allow replacing an already-published file with different contents under the same filename.

## 9. Verify the public release

In a fresh virtual environment outside the framework repository, install from PyPI:

```bash
python -m pip install skeleton-framework
python -m pip show skeleton-framework
skeleton --quickstart
skeleton --start
```

Confirm the package page and project metadata, and verify the complete client workflow one final time.

## Release checklist

- [ ] Distribution name and version are correct.
- [ ] Python package remains named `skeleton`; CLI command remains `skeleton`.
- [ ] License and README image are included and render correctly.
- [ ] Node tooling versions and internal dependency references are consistent.
- [ ] `python run.py --clean` and `python run.py --dist` succeed.
- [ ] `python -m twine check dist/*` succeeds.
- [ ] Wheel contents include all required templates, configuration, and tooling archives.
- [ ] Release-ready source is committed and pushed to GitHub.
- [ ] TestPyPI upload succeeds.
- [ ] Fresh external-environment installation and end-to-end client test succeed.
- [ ] Git tag/release identifies the tested source revision.
- [ ] The same artifacts are uploaded to PyPI.
- [ ] Fresh installation from PyPI and CLI workflow succeed.
