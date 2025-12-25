"""
Tests for link validation tool.

Covers URL extraction, validation logic, HTTP schemes, and error handling.
"""

from pathlib import Path

import pytest

from tools.validate_links import LinkValidator, ValidationResult


class TestLinkValidator:
    """Test suite for LinkValidator class."""

    def test_extract_markdown_links(self) -> None:
        """Test extraction of markdown-style links."""
        validator = LinkValidator()
        content = "[GitHub](https://github.com) and [Google](https://google.com)"
        links = validator.extract_links(content)
        assert "https://github.com" in links
        assert "https://google.com" in links

    def test_extract_html_links(self) -> None:
        """Test extraction of HTML href attributes."""
        validator = LinkValidator()
        content = '<a href="https://example.com">Link</a>'
        links = validator.extract_links(content)
        assert "https://example.com" in links

    def test_extract_mixed_links(self) -> None:
        """Test extraction of both markdown and HTML links."""
        validator = LinkValidator()
        content = '[Test](https://test.com) <img src="https://img.com/pic.png"/>'
        links = validator.extract_links(content)
        assert len(links) == 2
        assert "https://test.com" in links
        assert "https://img.com/pic.png" in links

    def test_extract_no_links(self) -> None:
        """Test extraction when no links are present."""
        validator = LinkValidator()
        content = "Just some plain text without any links"
        links = validator.extract_links(content)
        assert len(links) == 0

    def test_is_http_url(self) -> None:
        """Test HTTP/HTTPS URL detection."""
        validator = LinkValidator()
        assert validator._is_http_url("https://github.com")
        assert validator._is_http_url("http://example.com")
        assert not validator._is_http_url("mailto:test@example.com")
        assert not validator._is_http_url("/relative/path")
        assert not validator._is_http_url("ftp://files.example.com")

    def test_validate_valid_url(self) -> None:
        """Test validation of a known valid URL."""
        validator = LinkValidator()
        result = validator.validate_url("https://github.com")
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert "HTTP" in result.status_message

    def test_validate_invalid_url(self) -> None:
        """Test validation of a non-existent URL."""
        validator = LinkValidator()
        result = validator.validate_url("https://thisshouldnotexist12345.com")
        assert isinstance(result, ValidationResult)
        assert not result.is_valid

    def test_validate_empty_url(self) -> None:
        """Test validation of empty URL."""
        validator = LinkValidator()
        result = validator.validate_url("")
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert "Invalid URL format" in result.status_message

    def test_validate_url_too_long(self) -> None:
        """Test validation of URL exceeding maximum length."""
        validator = LinkValidator()
        long_url = "https://example.com/" + "a" * 3000
        result = validator.validate_url(long_url)
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
        assert "exceeds maximum length" in result.status_message

    def test_validate_file_not_found(self) -> None:
        """Test validation of non-existent file."""
        validator = LinkValidator()
        with pytest.raises(FileNotFoundError):
            validator.validate_file(Path("/nonexistent/file.md"))

    def test_validate_file_invalid_type(self) -> None:
        """Test validation with non-Path argument."""
        validator = LinkValidator()
        with pytest.raises(TypeError, match="filepath must be a Path object"):
            validator.validate_file("not_a_path")  # type: ignore
