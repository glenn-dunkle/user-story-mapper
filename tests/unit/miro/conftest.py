import pytest
import requests
from src.connectors.miro_connector import MiroConnector


class DummyMiroConnector:
    def __init__(self, token):
        self.token = token

    def connect(self):
        if self.token == "valid_token":
            return True
        if self.token == "network_error":
            raise requests.ConnectionError("Network error")
        raise ValueError("Invalid token")

    def getBoard(self, board_id):
        if self.token != "valid_token":
            raise ValueError("Invalid token")
        if board_id == "123":
            return {"id": "123", "name": "Test Board"}
        raise ValueError("Board not found")


@pytest.fixture
def miro():
    """Provide the MiroConnector class for tests."""
    # To switch to the dummy connector for isolated tests, return DummyMiroConnector instead.
    return MiroConnector
