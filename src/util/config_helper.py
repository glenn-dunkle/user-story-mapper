import tomllib as toml
import os
import boto3
import json
from botocore.exceptions import ClientError

# Define a global variable to store the configuration
CONFIG = {}

def load_config(config_file_path):
    """Loads the TOML configuration file into the global CONFIG variable."""
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")
    with open(config_file_path, 'rb') as f:
        CONFIG.update(toml.load(f))
        __get_aws_secret()

def __get_aws_secret():
    secret_name = CONFIG["aws"]["AWS_USM_SECRET"]
    region_name = CONFIG["aws"]["AWS_REGION"]

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    
    # Parse the secret string as JSON and update CONFIG
    try:
        secret_dict = json.loads(secret)
        
        # Update CONFIG with the secret values
        for key, value in secret_dict.items():
            
            # Add the KVP to CONFIG dictionary
            CONFIG["credentials"][key] = value
            
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse secret string as JSON: {e}")