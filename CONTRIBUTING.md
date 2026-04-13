# Contributing to clawphify

Thank you for your interest in contributing to clawphify! This project is a fork of [graphify](https://github.com/safishamsi/graphify) specialized for OpenClaw framework knowledge injection.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Install in development mode:
   ```bash
   pip install -e .
   ```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/clawphify.git
cd clawphify

# Install dependencies
pip install -e ".[all]"

# Test the CLI
clawphify --help
```

## Making Changes

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes and test them

3. Commit with clear messages:
   ```bash
   git commit -m "feat: add support for OpenClaw X.Y.Z"
   ```

4. Push to your fork and create a Pull Request

## Updating OpenClaw Graph

When OpenClaw releases a new version:

1. Update the graph in `clawphify/data/openclaw_graph.json`
2. Update `GRAPH_REPORT.md` with new features
3. Update version in `clawphify/__init__.py`

## Code Style

- Follow PEP 8 for Python code
- Add docstrings for new functions
- Keep the CLI interface consistent

## Reporting Issues

- Use GitHub Issues
- Include OpenClaw version and clawphify version
- Describe what you expected vs what happened

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
