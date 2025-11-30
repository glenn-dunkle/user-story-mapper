"""Exercise error handling for invalid credentials."""

import pytest


def test_invalid_credentials(miro):
    """Test handling invalid credentials."""
    connector = miro("invalid_token")
    with pytest.raises(ValueError):
        connector.getBoard("123")
