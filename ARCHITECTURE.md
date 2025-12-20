# Architecture

## Overview

This project is a GitHub profile README repository with Python-based tooling for quality assurance. The architecture follows strict engineering principles:

* **Python-first**: All tooling is Python-based for consistency
* **Type safety**: Full mypy compliance with strict mode
* **Zero technical debt**: No known issues left unaddressed
* **Separation of concerns**: Clear module boundaries
* **Defensive programming**: Explicit validation and error handling

## Module Structure

### Core Modules

#### `tools/config.py`
Configuration management with validation.

**Responsibilities:**
- Define configuration schema using dataclasses
- Validate configuration values on initialization
- Provide defaults
- (Future) Load from external configuration files

**Design patterns:**
- Dataclass for immutable configuration
- Post-init validation
- Factory pattern for loading

#### `tools/validate_links.py`
Link validation utility for README files.

**Responsibilities:**
- Extract URLs from markdown and HTML
- Validate HTTP/HTTPS links
- Retry logic with exponential backoff
- Report validation results
- CLI interface

**Design patterns:**
- Dependency injection (config)
- Strategy pattern (HEAD with GET fallback)
- Command pattern (CLI)

### Test Modules

#### `tests/test_config.py`
Tests for configuration management.

**Coverage:**
- Default values
- Custom values
- Validation of all constraints
- Edge cases

#### `tests/test_validate_links.py`
Tests for link validation.

**Coverage:**
- URL extraction
- Link validation
- Different URL schemes
- Edge cases

## Quality Standards

### Type Safety
- All functions have type annotations
- Mypy runs in strict mode
- External library stubs installed

### Testing
- pytest for test framework
- pytest-cov for coverage reporting
- Target: >80% code coverage

### Linting & Formatting
- **ruff**: Fast Python linter
- **black**: Code formatter (88 char line)
- **isort**: Import sorting
- **mypy**: Static type checking

### CI/CD
- Link validation on PRs and weekly schedule
- Snake animation generation daily
- Pre-commit hooks for local validation

## Configuration

Configuration is centralized in the `ValidationConfig` dataclass:

```python
@dataclass
class ValidationConfig:
    timeout: int = 10
    max_retries: int = 3
    retry_base: int = 2
    user_agent: str = "Mozilla/5.0 (compatible; LinkValidator/1.0)"
    max_url_length: int = 2048
    max_timeout: int = 300
```

All values are validated on initialization to prevent invalid states.

## Error Handling

Error handling follows these principles:

1. **Fail fast**: Invalid configuration raises ValueError immediately
2. **Graceful degradation**: Network errors are caught and reported
3. **Retry logic**: Transient errors trigger exponential backoff
4. **Clear messages**: Error messages indicate the failure reason

## Future Enhancements

Potential improvements aligned with engineering principles:

1. **Configuration files**: Load from YAML/JSON
2. **Parallel validation**: Validate multiple URLs concurrently
3. **Caching**: Cache validation results to reduce network calls
4. **Custom rules**: Allow custom validation rules per domain
5. **Metrics**: Export validation metrics for monitoring

## Contributing

When contributing, ensure:

1. All tests pass (`pytest`)
2. Type checking passes (`mypy tools/`)
3. Linting passes (`ruff check .`)
4. Formatting is correct (`black .`)
5. New features have tests
6. Documentation is updated
