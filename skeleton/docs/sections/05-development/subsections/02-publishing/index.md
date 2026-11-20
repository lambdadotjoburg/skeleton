## Publish

Install or update Twine & validate the generated artifacts:

```bash
python -m pip install --upgrade twine
python -m twine check dist/*
```

Upload the distribution to TestPyPI first:

```bash
python -m twine upload --repository testpypi dist/*
```

After verifying the TestPyPI installation, upload the **same artifacts** to PyPI:

```bash
python -m twine upload dist/*
```

Use the appropriate API token when prompted. TestPyPI and PyPI require separate credentials.

Never commit API tokens or other publishing credentials to the repository.

Do not rebuild or modify the distribution between the TestPyPI and PyPI uploads.