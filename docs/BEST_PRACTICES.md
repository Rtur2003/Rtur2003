# Best Practices Guide

This guide outlines best practices for working with this repository and its tooling.

## Code Quality

### Type Safety

**Always use type annotations:**

```python
# ✓ Good
def validate_url(self, url: str) -> ValidationResult:
    return ValidationResult(url, True, "HTTP 200")

# ✗ Avoid
def validate_url(self, url):
    return ValidationResult(url, True, "HTTP 200")
```

**Use mypy in strict mode:**

All code must pass `mypy --strict` checks. This catches potential bugs at development time.

### Documentation

**Write comprehensive docstrings:**

```python
def validate_file(self, filepath: Path) -> list[ValidationResult]:
    """
    Validate all HTTP/HTTPS links in a markdown file.

    Args:
        filepath: Path object pointing to the file to validate

    Returns:
        List of ValidationResult objects, one per URL found

    Raises:
        TypeError: If filepath is not a Path object
        FileNotFoundError: If the file does not exist
        ValueError: If path is not a file or contains invalid UTF-8
    """
```

**Document module purpose:**

Every module should have a clear docstring explaining its purpose and responsibilities.

### Error Handling

**Validate inputs early:**

```python
# ✓ Good - fail fast
def __post_init__(self) -> None:
    if self.timeout <= 0:
        raise ValueError("timeout must be positive")
```

**Provide specific error messages:**

```python
# ✓ Good
raise ValueError(f"timeout exceeds maximum allowed value of {self.max_timeout} seconds")

# ✗ Avoid
raise ValueError("Invalid timeout")
```

**Use appropriate exception types:**

- `ValueError` for invalid values
- `TypeError` for wrong types
- `FileNotFoundError` for missing files
- Custom exceptions for domain-specific errors

### Testing

**Test edge cases:**

```python
def test_validate_empty_url(self) -> None:
    """Test validation of empty URL."""
    validator = LinkValidator()
    result = validator.validate_url("")
    assert not result.is_valid
    assert "Invalid URL format" in result.status_message
```

**Test error paths:**

```python
def test_validate_file_not_found(self) -> None:
    """Test validation of non-existent file."""
    validator = LinkValidator()
    with pytest.raises(FileNotFoundError):
        validator.validate_file(Path("/nonexistent/file.md"))
```

**Use descriptive test names:**

Test names should clearly describe what is being tested:

```python
# ✓ Good
def test_validate_url_too_long(self) -> None:
def test_extract_mixed_links(self) -> None:

# ✗ Avoid
def test_1(self) -> None:
def test_validation(self) -> None:
```

### Code Organization

**Separate concerns:**

- Configuration in `config.py`
- Core logic in domain-specific modules
- CLI interfaces separated from business logic
- Tests mirror the source structure

**Use dataclasses for data structures:**

```python
@dataclass
class ValidationResult:
    """Result of URL validation."""
    url: str
    is_valid: bool
    status_message: str
```

**Keep functions focused:**

Each function should do one thing well. Extract complex logic into helper methods.

## Development Workflow

### Local Development

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install in editable mode:**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

### Before Committing

Run all quality checks:

```bash
# Linting
ruff check .

# Type checking
mypy tools/

# Formatting
black . --check
isort . --check

# Tests
pytest

# Or run all at once
pre-commit run --all-files
```

### Commit Messages

Follow conventional commit format:

```
feat: Add custom font support to README
fix: Correct type annotations in validate_links
docs: Add comprehensive usage examples
test: Add edge case tests for URL validation
refactor: Extract retry logic into separate method
```

### Pull Requests

**Before submitting:**

1. All tests pass
2. All linters pass
3. Code coverage maintained or improved
4. Documentation updated
5. CHANGELOG updated (if applicable)

**PR description should include:**

- What changed and why
- Related issue numbers
- Testing performed
- Breaking changes (if any)

## Configuration Management

### ValidationConfig Best Practices

**Use sensible defaults:**

```python
config = ValidationConfig()  # Use defaults for most cases
```

**Override only what you need:**

```python
config = ValidationConfig(
    timeout=30,      # Increase for slow servers
    max_retries=5    # More retries for flaky endpoints
)
```

**Validate configuration:**

All configuration is validated on creation. This prevents invalid states:

```python
# Raises ValueError immediately
config = ValidationConfig(timeout=-1)
```

## Link Validation Best Practices

### When to Validate

**Always validate:**

- Before merging PRs
- On scheduled CI runs (weekly)
- After updating external links
- Before major releases

**Don't validate:**

- On every commit (too slow)
- Internal/relative links (not HTTP/HTTPS)
- Links in code examples (unless they're meant to be live)

### Performance Considerations

**Batch validation is faster:**

```python
# ✓ Good - validate once per file
results = validator.validate_file(Path("README.md"))

# ✗ Avoid - multiple file reads
for url in urls:
    # Requires multiple file parses
    pass
```

**Adjust timeouts for known slow servers:**

```python
config = ValidationConfig(timeout=30)  # Default is 10s
validator = LinkValidator(config)
```

### Handling Failures

**Retry configuration:**

Transient network failures are retried automatically with exponential backoff.

**Known flaky links:**

For links that occasionally fail but are valid:
- Increase `max_retries`
- Increase `timeout`
- Add to ignore list (future feature)

## Security

### Input Validation

**Always validate untrusted input:**

```python
if not isinstance(url, str) or not url:
    return ValidationResult(url, False, "Error: Invalid URL format")
if len(url) > self.config.max_url_length:
    return ValidationResult(url, False, "Error: URL exceeds maximum length")
```

### Dependency Management

**Keep dependencies updated:**

```bash
pip list --outdated
```

**Pin versions in production:**

Use specific version numbers in `pyproject.toml` for production dependencies.

### Rate Limiting

The validator includes implicit rate limiting through:
- Retry delays with exponential backoff
- Sequential URL validation (no parallel requests)

For high-volume validation, consider:
- Adding delays between requests
- Implementing connection pooling
- Caching validation results

## Maintenance

### Regular Tasks

**Weekly:**
- Review CI failures
- Check for dependency updates
- Review open issues

**Monthly:**
- Update dependencies
- Review and update documentation
- Analyze code coverage

**Quarterly:**
- Major version updates
- Architecture review
- Performance profiling

### Monitoring

**Track metrics:**
- Test coverage percentage
- Link validation success rate
- Build times
- Issue resolution time

**Set up alerts for:**
- CI failures
- Broken links in README
- Security vulnerabilities

## Performance Optimization

### Current Performance

The validator is optimized for:
- Correctness over speed
- Reliability (with retries)
- Clear error reporting

### Future Optimizations

Consider implementing:
- Parallel URL validation
- Result caching
- Connection pooling
- Batch API requests

## Backwards Compatibility

### Maintain stability:**

- Don't break existing APIs
- Deprecate before removing
- Document breaking changes
- Version appropriately (semver)

### Adding features:**

- Add new parameters as optional
- Provide defaults for new config
- Update documentation
- Add migration guide if needed

## Documentation

### Keep docs updated:**

Update documentation when:
- Adding new features
- Changing behavior
- Fixing bugs that affect usage
- Improving examples

### Documentation structure:**

- README: Overview and quick start
- DEVELOPMENT: Setup and development
- USAGE: Detailed examples
- ARCHITECTURE: Design decisions
- CONTRIBUTING: Contribution process

## Community

### Code Review

**As a reviewer:**
- Check for test coverage
- Verify documentation updates
- Test the changes locally
- Provide constructive feedback

**As an author:**
- Respond to feedback promptly
- Update based on comments
- Keep PRs focused and small
- Test before requesting review

### Issues

**Creating issues:**
- Use clear, descriptive titles
- Provide reproduction steps
- Include environment details
- Add relevant labels

**Responding to issues:**
- Acknowledge quickly
- Ask clarifying questions
- Provide workarounds if available
- Link to related issues

## Conclusion

Following these best practices ensures:
- **Quality**: High-quality, maintainable code
- **Reliability**: Robust error handling and testing
- **Performance**: Efficient and scalable solutions
- **Community**: Welcoming and productive environment

Remember: Code is read more often than written. Write for clarity and maintainability.
