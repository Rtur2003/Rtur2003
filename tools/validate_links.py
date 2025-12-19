#!/usr/bin/env python3
"""
Link validation utility for README files.

Validates URLs in markdown files to detect broken links (404s).
Designed for CI/CD integration and local development checks.
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException


class LinkValidator:
    """Validates links in markdown content."""

    def __init__(self, timeout: int = 10):
        if timeout <= 0:
            raise ValueError("Timeout must be positive")
        if timeout > 300:
            raise ValueError("Timeout exceeds maximum allowed value of 300 seconds")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; LinkValidator/1.0)'
        })

    def extract_links(self, content: str) -> list[str]:
        """Extract all URLs from markdown content."""
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        html_links = re.findall(r'(?:href|src)="([^"]+)"', content)

        urls = [url for _, url in markdown_links] + html_links
        return [url for url in urls if self._is_http_url(url)]

    def _is_http_url(self, url: str) -> bool:
        """Check if URL is an HTTP/HTTPS URL."""
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')

    def validate_url(self, url: str) -> tuple[str, bool, str]:
        """
        Validate a single URL.

        Returns:
            Tuple of (url, is_valid, status_message)
        """
        if not url or not isinstance(url, str):
            return (url, False, "Error: Invalid URL format")
        if len(url) > 2048:
            return (url, False, "Error: URL exceeds maximum length")

        try:
            response = self.session.head(
                url,
                timeout=self.timeout,
                allow_redirects=True
            )

            # Some servers reject HEAD, try GET on client errors
            if response.status_code >= 400:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )

            is_valid = response.status_code < 400
            status = f"HTTP {response.status_code}"

            return (url, is_valid, status)

        except RequestException as e:
            return (url, False, f"Error: {type(e).__name__}")

    def validate_file(self, filepath: Path) -> list[tuple[str, bool, str]]:
        """Validate all links in a file."""
        if not isinstance(filepath, Path):
            raise TypeError("filepath must be a Path object")
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        if not filepath.is_file():
            raise ValueError(f"Path is not a file: {filepath}")

        try:
            content = filepath.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            raise ValueError(
                f"Unable to read file {filepath}: invalid UTF-8 encoding"
            ) from e

        urls = self.extract_links(content)

        results = []
        for url in urls:
            result = self.validate_url(url)
            results.append(result)

        return results


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python validate_links.py <markdown_file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])

    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    print(f"Validating links in: {filepath}\n")

    validator = LinkValidator()
    results = validator.validate_file(filepath)

    if not results:
        print("No HTTP/HTTPS links found.")
        sys.exit(0)

    failed = []
    passed = []

    for url, is_valid, status in results:
        if is_valid:
            passed.append((url, status))
            print(f"✓ {url} - {status}")
        else:
            failed.append((url, status))
            print(f"✗ {url} - {status}")

    print(f"\nResults: {len(passed)} passed, {len(failed)} failed")

    if failed:
        print("\nFailed links:")
        for url, status in failed:
            print(f"  - {url} ({status})")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
