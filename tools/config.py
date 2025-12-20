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
    """Configuration for link validation behavior."""

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
