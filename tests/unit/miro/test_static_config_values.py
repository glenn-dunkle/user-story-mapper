"""Validate static configuration values for the Miro connector."""


def test_static_config_values(miro):
    """Test that static configuration values can be loaded."""
    connector = miro("valid_token")
    assert connector.base_url == "https://api.miro.com/v2"
