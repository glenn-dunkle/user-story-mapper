import os
import re
import logging
from src.util.config_helper import CONFIG

class LoggerHelper:
    def __init__(self, name=None):
        self.name = name if name else "default_logger"
        self.log_folder = CONFIG["logging"]["LOG_FOLDER"]
        self.log_format = CONFIG["logging"]["LOG_FORMAT"]
        self.log_date_format = CONFIG["logging"]["LOG_DATE_FORMAT"]
        
    def __setLogLevel(self):
        log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        return log_levels.get(CONFIG["logging"]["LOG_LEVEL"].upper(), logging.INFO)
    
    def __setLogLocation(self, log_name=None):
        self.log_file = f"{log_name}{CONFIG["logging"]["LOG_FILE_EXT"]}" if log_name else "default.log"

        # Create the log directory if it doesn't exist
        os.makedirs(self.log_folder, exist_ok=True)
        return os.path.join(self.log_folder, self.log_file)

    def getLogger(self, log_name=None):
        # Create or get the logger instance
        self.logger = logging.getLogger(self.name)

        # Set the minimul log level for all logging
        self.logger.setLevel(self.__setLogLevel())

        # Create a file handler and set its level to the configured log level. 
        # For now, this is the same as the overall log level
        file_handler = logging.FileHandler(self.__setLogLocation(log_name=log_name))
        file_handler.setLevel(self.__setLogLevel())

        # Create the format mask for the log file and attach to the file handler
        formatter = logging.Formatter(self.log_format, datefmt=self.log_date_format)
        file_handler.setFormatter(formatter)

        # Attach the file handler to the logger
        self.logger.addHandler(file_handler)

        return self.logger

    def getLogLevel(self, file_handler: logging.FileHandler = None):
        print(f"File handler Level: {file_handler.level}")
        return  file_handler.level
    
    # TODO: I think this code overrides the purpose for selective level logging. 
    # Probably needs to be removed.
    def logMessage(self, message=None):
        match self.logger.level: # .getLogLevel(self.logger.handlers[0]):
            case logging.DEBUG:
                self.logger.debug(self._obfuscate(message))
            case logging.INFO:
                self.logger.info(self._obfuscate(message))
            case logging.WARNING:
                self.logger.warning(self._obfuscate(message))
            case logging.ERROR:
                self.logger.error(self._obfuscate(message))
            case logging.CRITICAL:
                self.logger.critical(self._obfuscate(message))
            case _:
                self.logger.info(self._obfuscate(message))

    def _obfuscate(self, message):
        """Obfuscate sensitive information in the message before logging."""
        if not isinstance(message, str):
            return message

        # Common patterns for sensitive data
        patterns = {
        # Match API keys in various formats (JSON, dict, string)
            r'(["\']?(MIRO|JIRA|OPENAI)_API_KEY["\']?\s*[:=]\s*["\']?)([^"\'\s,}\]]+)(["\']?)': r'\1***REDACTED***\4',
            
            # Environment variables style keys (more general pattern)
            r'(["\']?[A-Z_]+(KEY|TOKEN|SECRET|PASSWORD)["\']?\s*[:=]\s*["\']?)([^"\'\s,}\]]+)(["\']?)': r'\1***REDACTED***\4',
            
            # API Keys, Tokens, and Auth headers (case insensitive)
            r'(?i)(["\']?(api[-_]?key|auth[-_]?token|bearer)["\']?\s*[:=]\s*["\']?)([^"\'\s,}\]]+)(["\']?)': r'\1***REDACTED***\4',

            # Passwords
            r'(password|passwd)["\s:]+([^"\s,}\]]+)': r'\1: ***REDACTED***',

            # Email addresses
            r'[\w\.-]+@[\w\.-]+': '***EMAIL@REDACTED***',

            # Credit card numbers
            r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b': '***CARD-REDACTED***',

            # AWS keys
            r'(AKIA|ASIA)[A-Z0-9]{16}': '***AWS-KEY-REDACTED***',

            # Private keys
            r'-----BEGIN (?:RSA )?PRIVATE KEY-----[^-]+-----END (?:RSA )?PRIVATE KEY-----': '***PRIVATE-KEY-REDACTED***'
        }

        obfuscated = message
        for pattern, replacement in patterns.items():
            obfuscated = re.sub(pattern, replacement, obfuscated, flags=re.IGNORECASE)
        
        return obfuscated
# Example usage:
# logger = Logger("my_logger").get_logger()
# logger.info("This is an info message.")
# logger.error("This is an error message.")
# logger.debug("This is a debug message.")
# logger.warning("This is a warning message.")
# logger.critical("This is a critical message.")
# logger.exception("This is an exception message with traceback.")
# logger.log(logging.INFO, "This is a log message with level INFO.")
# logger.log(logging.ERROR, "This is a log message with level ERROR.")
# logger.log(logging.DEBUG, "This is a log message with level DEBUG.")
# logger.log(logging.WARNING, "This is a log message with level WARNING.")
# logger.log(logging.CRITICAL, "This is a log message with level CRITICAL.")
