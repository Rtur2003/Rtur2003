"""
Tests for link validation tool.
"""

import pytest
from pathlib import Path
from tools.validate_links import LinkValidator


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
        url, is_valid, status = validator.validate_url("https://github.com")
        assert is_valid
        assert "HTTP" in status
    
    def test_validate_invalid_url(self):
        validator = LinkValidator()
        url, is_valid, status = validator.validate_url("https://thisshouldnotexist12345.com")
        assert not is_valid
