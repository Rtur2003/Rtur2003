# Contributing Guidelines

Thank you for considering contributing to this project!

## Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/your-username/Rtur2003.git
   cd Rtur2003
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**

   ```bash
   pre-commit install
   ```

## Development Workflow

### Code Quality Standards

All contributions must pass:

* **Black** - Code formatting (88 char line length)
* **Ruff** - Linting and code quality
* **isort** - Import organization
* **mypy** - Static type checking
* **pytest** - All tests must pass

Run quality checks:

```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy tools/

# Run tests
pytest
```

### Making Changes

1. **Create a topic branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make atomic commits**

   Each commit should represent one logical change:
   * One function modification
   * One bug fix
   * One refactor step

   Use descriptive commit messages:

   ```
   scope: precise description of change

   Examples:
   - validation: add url length checking
   - refactor: extract validation logic
   - fix: handle edge case in link parsing
   ```

3. **Test your changes**

   ```bash
   pytest tests/
   ```

4. **Run pre-commit checks**

   ```bash
   pre-commit run --all-files
   ```

### Pull Request Process

1. Ensure all tests pass and code quality checks succeed
2. Update documentation if needed
3. Create a pull request with:
   * Clear description of changes
   * Reference to any related issues
   * List of what was changed and why

## Code Style

* Follow existing patterns in the codebase
* Use type annotations for all functions
* Add docstrings for public APIs
* Keep functions focused and single-purpose
* Prefer explicit over implicit

## Questions?

Open an issue for discussion before making major changes.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
