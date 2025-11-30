"""Ensure the connector allows successful connections when enabled."""


def test_connect_enabled(miro):
    """Test successful connection when enabled."""
    connector = miro("valid_token")
    assert connector.connect() is True
