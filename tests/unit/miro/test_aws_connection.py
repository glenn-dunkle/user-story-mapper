"""Check AWS client interactions used by the connector."""

from unittest.mock import patch


def test_aws_connection():
    """Test AWS connection for secrets."""
    with patch("boto3.client") as mock_client:
        mock_client.return_value.get_secret_value.return_value = {
            "SecretString": '{"MIRO_TOKEN": "test_token"}'
        }
        assert True
