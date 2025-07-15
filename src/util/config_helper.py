import tomllib as toml
import os

# Define a global variable to store the configuration
CONFIG = {}

def load_config(config_file_path):
    """Loads the TOML configuration file into the global CONFIG variable."""
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")
    with open(config_file_path, 'rb') as f:
        CONFIG.update(toml.load(f))

# TODO add debug print of running configimport tomllib as toml
import os

# Define a global variable to store the configuration
CONFIG = {}

def load_config(config_file_path="/app/pyproject.toml"):
    """Loads the TOML configuration file into the global CONFIG variable."""
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")
    with open(config_file_path, 'rb') as f:
        CONFIG.update(toml.load(f))