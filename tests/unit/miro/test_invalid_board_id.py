"""Cover invalid board identifier scenarios."""

import pytest


def test_invalid_board_id(miro):
    """Test handling invalid board ID."""
    connector = miro("valid_token")
    with pytest.raises(ValueError):
        connector.getBoard("invalid_id")
