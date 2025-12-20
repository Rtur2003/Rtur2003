# Development Guide

## Overview

This repository contains the GitHub profile README for Hasan Arthur Altuntaş, along with Python-based tooling for quality assurance and link validation.

## Quick Links

* [Contributing Guidelines](CONTRIBUTING.md)
* [Code of Conduct](CODE_OF_CONDUCT.md)
* [License](LICENSE)

## Project Structure

```
.
├── tools/               # Python utilities
│   ├── config.py        # Configuration management
│   └── validate_links.py  # Link validation tool
├── tests/              # Unit tests
│   ├── test_config.py
│   └── test_validate_links.py
├── .github/            # GitHub workflows
│   └── workflows/
│       ├── snake.yml   # Contribution graph generator
│       └── link-check.yml  # Link validation CI
├── README.md           # Profile page
├── DEVELOPMENT.md      # This file
├── CONTRIBUTING.md     # Contribution guidelines
├── CODE_OF_CONDUCT.md  # Community guidelines
├── LICENSE             # MIT License
├── pyproject.toml      # Python project config
└── requirements-dev.txt # Development dependencies
```

## Setup

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -e ".[dev]"
```

3. Install pre-commit hooks:

```bash
pre-commit install
```

## Tools

### Link Validator

Validates all HTTP/HTTPS links in markdown files.

**Usage:**

```bash
python tools/validate_links.py README.md
```

**Features:**
- Extracts links from markdown and HTML
- HEAD request with GET fallback
- Configurable timeouts and retry logic
- Clear pass/fail reporting
- Exit code for CI integration
- Centralized configuration management

## Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=tools --cov-report=term-missing
```

## Code Quality

### Linting

```bash
ruff check .
```

### Formatting

```bash
black .
isort .
```

### Type Checking

```bash
mypy tools/
```

### Pre-commit

All checks run automatically on commit. Manual run:

```bash
pre-commit run --all-files
```

## CI/CD

- **Snake Animation**: Generates contribution graph daily
- **Link Checker**: Validates links on PR and scheduled runs

## Principles

This project follows strict engineering discipline:

- **Python-first**: All tooling in Python
- **Atomic commits**: One logical change per commit
- **Zero technical debt**: No known issues left unaddressed
- **Type safety**: Full mypy compliance with strict settings
- **Defensive validation**: Explicit guards and error handling
- **Structured logging**: Operational visibility at all levels

## Architecture

### Validation Module

The link validator (`tools/validate_links.py`) follows these design principles:

* **Separation of concerns**: 
  - Configuration in `tools/config.py`
  - Validation logic in `tools/validate_links.py`
  - CLI interface separated from core logic
* **Type safety**: Full type annotations with dataclasses
* **Robustness**: Input validation, retry logic, timeout bounds
* **Observability**: Structured logging for debugging
* **Testability**: Pure functions with clear interfaces and dependency injection
* **Configurability**: Centralized configuration with validation

### Quality Gates

Every commit must pass:

1. **Ruff** - Code quality and style
2. **Black** - Consistent formatting
3. **isort** - Import organization
4. **mypy** - Static type checking
5. **pytest** - All unit tests

These run automatically via pre-commit hooks and CI.
