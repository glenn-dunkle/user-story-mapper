"""Ensure the connector blocks access when disabled."""

import pytest


def test_connect_disabled(miro):
    """Test connection disabled."""
    connector = miro("invalid_token")
    with pytest.raises(ValueError):
        connector.connect()
