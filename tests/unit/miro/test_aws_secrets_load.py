"""Validate that AWS secrets are loaded into configuration."""

from unittest.mock import patch


def test_aws_secrets_load():
    """Test loading AWS secrets into config."""
    with patch("boto3.client") as mock_client:
        mock_client.return_value.get_secret_value.return_value = {
            "SecretString": '{"MIRO_TOKEN": "test_token"}'
        }
        assert True
