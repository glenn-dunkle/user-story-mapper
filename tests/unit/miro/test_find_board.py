"""Ensure existing boards can be retrieved."""


def test_find_board(miro):
    """Test finding board with valid board ID."""
    connector = miro("valid_token")
    board = connector.getBoard("123")
    assert board["id"] == "123"
    assert board["name"] == "Test Board"
