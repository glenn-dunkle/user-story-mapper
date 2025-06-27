from src.util.config_helper import CONFIG
from src.util.logger_helper import LoggerHelper

class ErrLogger(LoggerHelper):
    def __init__(self):
        self.name = CONFIG["logging"]["LOG_ERR_NAME"]
        super().__init__("err_logger")
        
    def getLogger(self, log_name=None):
        log_name = log_name if log_name else f"{CONFIG["logging"]["LOG_ERR_NAME"]}"
        super().getLogger(log_name)
  
        # Log the initialization
        self.logMessage(f">>>>>> Error log initialized: {self.name} <<<<<<")

        return ErrLogger
    
    def logMessage(self, message):
#        self.logger.log(self.logger.level, message)
        super().logMessage(message)
        