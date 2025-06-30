import os
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
                self.logger.debug(message)
            case logging.INFO:
                self.logger.info(message)
            case logging.WARNING:
                self.logger.warning(message)
            case logging.ERROR:
                self.logger.error(message)
            case logging.CRITICAL:
                self.logger.critical(message)
            case _:
                self.logger.info(message)

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
