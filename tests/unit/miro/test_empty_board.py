"""Confirm the connector handles empty boards correctly."""

from unittest.mock import patch


def test_empty_board(miro):
    """Test handling board with no sticky notes."""
    with patch.object(miro, "get_sticky_notes", return_value=[]):
        connector = miro("valid_token")
        sticky_notes = connector.get_sticky_notes("123")
        assert len(sticky_notes) == 0
