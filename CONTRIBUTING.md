# Contributing to Steadfast Courier Python SDK

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/steadfast-python.git`
3. Create a virtual environment: `python3 -m venv venv`
4. Activate it: `source venv/bin/activate`
5. Install dev dependencies: `pip install -r requirements-dev.txt`
6. Install pre-commit hooks: `pre-commit install`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Run quality checks: `./scripts/quality-check.sh`
4. Commit with legacy-style messages: `git commit -m "Add feature description"`
5. Push to your fork: `git push origin feature/your-feature`
6. Create a Pull Request

## Code Quality Standards

All code must pass:

- **Black** - Code formatting (88 character line length)
- **Flake8** - Linting
- **MyPy** - Type checking (strict mode)
- **Pytest** - All tests must pass

Run checks manually:
```bash
./scripts/quality-check.sh
```

## Testing

- Write tests for all new features
- Maintain 80%+ code coverage
- Test edge cases and error scenarios
- Use descriptive test names

Run tests:
```bash
pytest tests/ -v
pytest tests/ --cov=steadfast --cov-report=html
```

## Type Hints

All functions must have type hints:

```python
def create_order(
    invoice: str,
    recipient_name: str,
    cod_amount: float
) -> Order:
    """Create an order."""
    pass
```

## Documentation

- Update docstrings for all functions
- Add examples for new features
- Update relevant documentation files
- Keep README.md current

## Commit Messages

Use legacy-style commit messages without emojis:

```
Add feature description
Fix bug in module
Update documentation
```

## Pull Request Process

1. Update documentation
2. Add/update tests
3. Ensure all checks pass
4. Provide clear PR description
5. Link related issues

## Code of Conduct

Be respectful and professional. We're committed to providing a welcoming environment.

## Questions?

Open an issue or contact the maintainers.

Thank you for contributing!
