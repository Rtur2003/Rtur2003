# Development Guide

## Overview

This repository contains the GitHub profile README for Hasan Arthur Altuntaş, along with Python-based tooling for quality assurance and link validation.

## Project Structure

```
.
├── tools/               # Python utilities
│   └── validate_links.py  # Link validation tool
├── tests/              # Unit tests
│   └── test_validate_links.py
├── .github/            # GitHub workflows
│   └── workflows/
│       ├── snake.yml   # Contribution graph generator
│       └── link-check.yml  # Link validation CI
├── README.md           # Profile page
└── pyproject.toml      # Python project config
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
- Clear pass/fail reporting
- Exit code for CI integration

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
- **Defensive validation**: Explicit guards and error handling
