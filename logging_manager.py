import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler

class logger_manager:
    def __init__(self) -> None:
        self.data_path = "./"
        self.logger = logging.getLogger("tty")
        stdlogHandler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(stdlogHandler)
        
    def initLogger(self) -> logging.Logger:
        log_file_name = f"{self.data_path}/log/tty.log"
        os.makedirs(os.path.dirname(log_file_name), exist_ok=True)
        rotate_handler = TimedRotatingFileHandler(log_file_name, when="d", interval=1, backupCount=10, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s",
                        "%Y-%m-%d %H:%M:%S")
        rotate_handler.setFormatter(formatter)
        self.logger.addHandler(rotate_handler)
        self.logger.setLevel(logging.INFO)
        return self.logger