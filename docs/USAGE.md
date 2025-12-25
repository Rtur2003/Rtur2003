# Usage Examples

This document provides detailed examples of using the tools in this repository.

## Link Validation Tool

The link validation tool checks HTTP/HTTPS links in markdown files to ensure they are accessible.

### Basic Usage

Validate a single file:

```bash
python tools/validate_links.py README.md
```

### Example Output

```
Validating links in: README.md

Found 25 HTTP/HTTPS links to validate
✓ https://github.com/Rtur2003 - HTTP 200
✓ https://hasanarthuraltuntas.com.tr - HTTP 200
✓ https://www.youtube.com/@HasanArthurAltunta%C5%9F - HTTP 200
✗ https://example-broken-link.com - Error: ConnectionError

Results: 24 passed, 1 failed

Failed links:
  - https://example-broken-link.com (Error: ConnectionError)
```

### Advanced Usage

#### Custom Configuration

```python
from pathlib import Path
from tools.config import ValidationConfig
from tools.validate_links import LinkValidator

# Create custom configuration
config = ValidationConfig(
    timeout=20,          # 20 second timeout
    max_retries=5,       # Retry up to 5 times
    retry_base=3,        # Exponential backoff base
    max_wait_time=60     # Maximum 60 seconds between retries
)

# Use custom config
validator = LinkValidator(config=config)
results = validator.validate_file(Path("README.md"))

# Process results
for result in results:
    print(f"URL: {result.url}")
    print(f"Valid: {result.is_valid}")
    print(f"Status: {result.status_message}")
```

#### Programmatic Validation

```python
from tools.validate_links import LinkValidator

validator = LinkValidator()

# Validate a single URL
result = validator.validate_url("https://github.com")
if result.is_valid:
    print(f"URL is accessible: {result.status_message}")
else:
    print(f"URL failed: {result.status_message}")

# Extract links from markdown content
content = """
# My Document
Check out [GitHub](https://github.com) and [Google](https://google.com)
"""
links = validator.extract_links(content)
print(f"Found {len(links)} links: {links}")
```

#### Batch Validation

```python
from pathlib import Path
from tools.validate_links import LinkValidator

validator = LinkValidator()

# Validate multiple files
files = [
    Path("README.md"),
    Path("CONTRIBUTING.md"),
    Path("ARCHITECTURE.md")
]

all_results = []
for filepath in files:
    print(f"\nValidating {filepath}...")
    results = validator.validate_file(filepath)
    all_results.extend(results)

# Summary
total = len(all_results)
valid = sum(1 for r in all_results if r.is_valid)
invalid = total - valid

print(f"\nTotal: {total} URLs")
print(f"Valid: {valid}")
print(f"Invalid: {invalid}")
```

### Integration with CI/CD

#### GitHub Actions

The tool is integrated into CI/CD via `.github/workflows/link-check.yml`:

```yaml
name: Link Validation

on:
  pull_request:
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  validate-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -e .
      - name: Validate README links
        run: python tools/validate_links.py README.md
```

### Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `timeout` | 10 | HTTP request timeout in seconds (1-300) |
| `max_retries` | 3 | Number of retry attempts for transient failures |
| `retry_base` | 2 | Base for exponential backoff (e.g., 2^attempt) |
| `max_wait_time` | 30 | Maximum seconds to wait between retries |
| `user_agent` | LinkValidator/1.0 | User-Agent header for requests |
| `max_url_length` | 2048 | Maximum URL length to validate |

### Error Handling

The tool provides specific error messages:

- **Invalid URL format**: Empty or malformed URL
- **URL exceeds maximum length**: URL is too long
- **HTTP 4xx/5xx**: Server returned error status
- **ConnectionError**: Unable to reach server
- **Timeout**: Request took too long
- **RequestException**: Other HTTP-related errors

### Best Practices

1. **Regular validation**: Run link checks weekly via scheduled CI
2. **PR validation**: Check links in PRs before merging
3. **Custom timeouts**: Increase timeout for slow servers
4. **Retry configuration**: Adjust retries for flaky endpoints
5. **Ignore patterns**: Use `.linkvalidatorignore` for known issues (future feature)

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=tools --cov-report=term-missing
```

### Run Specific Test

```bash
pytest tests/test_validate_links.py::TestLinkValidator::test_validate_valid_url
```

## Linting and Formatting

### Ruff (Linting)

```bash
ruff check .
```

Auto-fix issues:

```bash
ruff check . --fix
```

### Black (Formatting)

```bash
black .
```

Check without modifying:

```bash
black . --check
```

### isort (Import Sorting)

```bash
isort .
```

### mypy (Type Checking)

```bash
mypy tools/
```

### Pre-commit (All Checks)

Run all quality checks:

```bash
pre-commit run --all-files
```

## Troubleshooting

### Common Issues

#### Import Error

**Problem:** `ModuleNotFoundError: No module named 'tools'`

**Solution:**
```bash
pip install -e .
```

#### Type Checking Fails

**Problem:** `Library stubs not installed for "requests"`

**Solution:**
```bash
pip install -e ".[dev]"
```

The dev dependencies include all required type stubs.

#### Tests Fail with Network Errors

**Problem:** Tests timeout or fail due to network issues

**Solution:** This is expected for transient network errors. The validator includes retry logic.

#### Pre-commit Hook Fails

**Problem:** Pre-commit hooks fail on commit

**Solution:**
```bash
pre-commit run --all-files
# Fix reported issues
git add .
git commit
```

### Getting Help

1. Check [DEVELOPMENT.md](../DEVELOPMENT.md) for setup instructions
2. Review [CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines
3. Open an issue on GitHub for bugs or feature requests
