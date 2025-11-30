"""Handle network error recovery logic."""

import requests
import pytest


def test_network_error(miro):
    """Test handling network errors."""
    connector = miro("network_error")
    with pytest.raises(requests.ConnectionError):
        connector.connect()
