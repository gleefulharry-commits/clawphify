# Publishing to PyPI

## Prerequisites

```bash
# Install build tools
pip install build twine

# Create PyPI account at https://pypi.org/account/register/
# Get API token from https://pypi.org/manage/account/token/
```

## Build and Publish

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build package
python -m build

# Check package
twine check dist/*

# Upload to Test PyPI first (optional)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## GitHub Actions 自动发布

Create `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: |
        python -m build
        twine upload dist/*
```

Add `PYPI_API_TOKEN` to GitHub Secrets:
1. Go to Settings → Secrets and variables → Actions
2. New repository secret
3. Name: `PYPI_API_TOKEN`
4. Value: Your PyPI API token
