# Contributing to phoenix-mcp-eval

Thank you for your interest in contributing! This project is part of the MCP (Model Context Protocol) ecosystem for Arize Phoenix LLM observability.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/phoenix-mcp-eval.git`
3. Create a feature branch: `git checkout -b feat/your-feature`
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes and add tests
6. Commit with a clear message: `git commit -m 'feat: add your feature'`
7. Push and open a Pull Request

## Development Setup

```bash
pip install -r requirements.txt
export PHOENIX_API_KEY=your_key
export PHOENIX_BASE_URL=https://app.phoenix.arize.com
python server.py
```

## Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` new feature
- `fix:` bug fix
- `docs:` documentation
- `chore:` maintenance
- `refactor:` code restructure

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to all public functions
- Keep functions focused and small

## Reporting Issues

Open a GitHub issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS

## Security

Do **not** open public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md).

## License

By contributing, you agree your contributions will be licensed under the MIT License.
