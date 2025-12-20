"""
Tests for link validation tool.
"""

from tools.validate_links import LinkValidator, ValidationResult


class TestLinkValidator:

    def test_extract_markdown_links(self):
        validator = LinkValidator()
        content = "[GitHub](https://github.com) and [Google](https://google.com)"
        links = validator.extract_links(content)
        assert "https://github.com" in links
        assert "https://google.com" in links

    def test_extract_html_links(self):
        validator = LinkValidator()
        content = '<a href="https://example.com">Link</a>'
        links = validator.extract_links(content)
        assert "https://example.com" in links

    def test_is_http_url(self):
        validator = LinkValidator()
        assert validator._is_http_url("https://github.com")
        assert validator._is_http_url("http://example.com")
        assert not validator._is_http_url("mailto:test@example.com")
        assert not validator._is_http_url("/relative/path")

    def test_validate_valid_url(self):
        validator = LinkValidator()
        result = validator.validate_url("https://github.com")
        assert isinstance(result, ValidationResult)
        assert result.is_valid
        assert "HTTP" in result.status_message

    def test_validate_invalid_url(self):
        validator = LinkValidator()
        result = validator.validate_url("https://thisshouldnotexist12345.com")
        assert isinstance(result, ValidationResult)
        assert not result.is_valid
