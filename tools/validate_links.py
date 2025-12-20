#!/usr/bin/env python3
"""
Link validation utility for README files.

Validates URLs in markdown files to detect broken links (404s).
Designed for CI/CD integration and local development checks.
"""

import logging
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import requests
from requests.exceptions import RequestException

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of URL validation."""

    url: str
    is_valid: bool
    status_message: str


class LinkValidator:
    """Validates links in markdown content."""

    RETRY_BASE = 2
    MAX_RETRIES = 3

    def __init__(self, timeout: int = 10):
        if timeout <= 0:
            raise ValueError("Timeout must be positive")
        if timeout > 300:
            raise ValueError("Timeout exceeds maximum allowed value of 300 seconds")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (compatible; LinkValidator/1.0)"}
        )
        logger.debug(f"LinkValidator initialized with timeout={timeout}s")

    def extract_links(self, content: str) -> list[str]:
        """Extract all URLs from markdown content."""
        markdown_links = re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", content)
        html_links = re.findall(r'(?:href|src)="([^"]+)"', content)

        urls = [url for _, url in markdown_links] + html_links
        return [url for url in urls if self._is_http_url(url)]

    def _is_http_url(self, url: str) -> bool:
        """Check if URL is an HTTP/HTTPS URL."""
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https")

    def validate_url(self, url: str) -> ValidationResult:
        """
        Validate a single URL.

        Returns:
            ValidationResult with url, validity status, and message
        """
        if not isinstance(url, str) or not url:
            return ValidationResult(url, False, "Error: Invalid URL format")
        if len(url) > 2048:
            return ValidationResult(url, False, "Error: URL exceeds maximum length")

        for attempt in range(self.MAX_RETRIES):
            try:
                response = self.session.head(
                    url, timeout=self.timeout, allow_redirects=True
                )

                # Some servers reject HEAD, try GET on client errors
                if response.status_code >= 400:
                    response = self.session.get(
                        url, timeout=self.timeout, allow_redirects=True
                    )

                is_valid = response.status_code < 400
                status = f"HTTP {response.status_code}"

                return ValidationResult(url, is_valid, status)

            except (
                requests.exceptions.Timeout,
                requests.exceptions.ConnectionError,
            ) as e:
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_BASE**attempt
                    logger.debug(
                        f"Retry {attempt + 1}/{self.MAX_RETRIES} for {url} "
                        f"after {wait_time}s"
                    )
                    time.sleep(wait_time)
                    continue
                return ValidationResult(url, False, f"Error: {type(e).__name__}")
            except RequestException as e:
                return ValidationResult(url, False, f"Error: {type(e).__name__}")

        return ValidationResult(url, False, "Error: Unexpected validation failure")

    def validate_file(self, filepath: Path) -> list[ValidationResult]:
        """Validate all links in a file."""
        if not isinstance(filepath, Path):
            raise TypeError("filepath must be a Path object")
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        if not filepath.is_file():
            raise ValueError(f"Path is not a file: {filepath}")

        logger.info(f"Validating links in file: {filepath}")

        try:
            content = filepath.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            raise ValueError(
                f"Unable to read file {filepath}: invalid UTF-8 encoding"
            ) from e

        urls = self.extract_links(content)
        logger.info(f"Found {len(urls)} HTTP/HTTPS links to validate")

        results = []
        for url in urls:
            result = self.validate_url(url)
            results.append(result)

        return results


def main() -> None:
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

    for result in results:
        if result.is_valid:
            passed.append((result.url, result.status_message))
            print(f"✓ {result.url} - {result.status_message}")
        else:
            failed.append((result.url, result.status_message))
            print(f"✗ {result.url} - {result.status_message}")

    print(f"\nResults: {len(passed)} passed, {len(failed)} failed")

    if failed:
        print("\nFailed links:")
        for url, status in failed:
            print(f"  - {url} ({status})")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
