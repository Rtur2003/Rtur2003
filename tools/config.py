"""
Configuration management for link validation tooling.

Provides centralized configuration with validation and defaults.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class ValidationConfig:
    """
    Configuration for link validation behavior.

    Attributes:
        timeout: HTTP request timeout in seconds (1-300)
        max_retries: Number of retry attempts for transient failures (0+)
        retry_base: Base for exponential backoff calculation (1+)
        max_wait_time: Maximum wait time between retries in seconds (1+)
        user_agent: User-Agent header for HTTP requests
        max_url_length: Maximum allowed URL length in characters (1+)
        max_timeout: Maximum allowed timeout value in seconds

    Raises:
        ValueError: If any configuration value violates constraints
    """

    timeout: int = 10
    max_retries: int = 3
    retry_base: int = 2
    max_wait_time: int = 30
    user_agent: str = "Mozilla/5.0 (compatible; LinkValidator/1.0)"
    max_url_length: int = 2048
    max_timeout: int = 300

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
        if self.timeout > self.max_timeout:
            raise ValueError(
                f"timeout exceeds maximum allowed value of {self.max_timeout} seconds"
            )
        if self.max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if self.retry_base < 1:
            raise ValueError("retry_base must be at least 1")
        if self.max_url_length <= 0:
            raise ValueError("max_url_length must be positive")
        if self.max_wait_time <= 0:
            raise ValueError("max_wait_time must be positive")


def load_config(config_path: Optional[Path] = None) -> ValidationConfig:
    """
    Load configuration from file or return defaults.

    Args:
        config_path: Optional path to configuration file.
                    Currently not implemented - will be added in future version.

    Returns:
        ValidationConfig instance with loaded or default values

    Note:
        Configuration file loading is planned for a future release.
        Currently always returns default configuration.
    """
    if config_path:
        logger.warning(
            f"Configuration file loading not yet implemented. "
            f"Ignoring config path: {config_path}"
        )

    return ValidationConfig()
