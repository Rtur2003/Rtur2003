"""
Tests for configuration management.
"""

import pytest

from tools.config import ValidationConfig, load_config


class TestValidationConfig:
    def test_default_values(self) -> None:
        config = ValidationConfig()
        assert config.timeout == 10
        assert config.max_retries == 3
        assert config.retry_base == 2
        assert config.max_wait_time == 30
        assert config.max_url_length == 2048
        assert config.max_timeout == 300

    def test_custom_values(self) -> None:
        config = ValidationConfig(timeout=20, max_retries=5)
        assert config.timeout == 20
        assert config.max_retries == 5

    def test_validation_negative_timeout(self) -> None:
        with pytest.raises(ValueError, match="timeout must be positive"):
            ValidationConfig(timeout=-1)

    def test_validation_zero_timeout(self) -> None:
        with pytest.raises(ValueError, match="timeout must be positive"):
            ValidationConfig(timeout=0)

    def test_validation_timeout_exceeds_max(self) -> None:
        with pytest.raises(ValueError, match="timeout exceeds maximum"):
            ValidationConfig(timeout=400)

    def test_validation_negative_retries(self) -> None:
        with pytest.raises(ValueError, match="max_retries must be non-negative"):
            ValidationConfig(max_retries=-1)

    def test_validation_invalid_retry_base(self) -> None:
        with pytest.raises(ValueError, match="retry_base must be at least 1"):
            ValidationConfig(retry_base=0)

    def test_validation_invalid_max_url_length(self) -> None:
        with pytest.raises(ValueError, match="max_url_length must be positive"):
            ValidationConfig(max_url_length=-1)

    def test_validation_invalid_max_wait_time(self) -> None:
        with pytest.raises(ValueError, match="max_wait_time must be positive"):
            ValidationConfig(max_wait_time=0)


class TestLoadConfig:
    def test_load_config_defaults(self) -> None:
        config = load_config()
        assert isinstance(config, ValidationConfig)
        assert config.timeout == 10

    def test_load_config_nonexistent_path(self) -> None:
        from pathlib import Path

        config = load_config(Path("/nonexistent/path"))
        assert isinstance(config, ValidationConfig)
        assert config.timeout == 10
