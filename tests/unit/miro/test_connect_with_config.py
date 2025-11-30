"""Verify the connector can authenticate using configuration values."""

from unittest.mock import patch


def test_connect_with_config(miro):
    """Test connection using config credentials."""
    with patch("src.util.config_helper.CONFIG", {"credentials": {"MIRO_TOKEN": "valid_token"}}):
        connector = miro("valid_token")
        assert connector.connect() is True
