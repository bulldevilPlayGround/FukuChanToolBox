import logging
import os
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(LogLevel.DEBUG.value)
        self._create_console_handler()

    def _create_console_handler(self):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(LogLevel.DEBUG.value)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    def _create_file_handler(self):
        log_dir = os.getcwd()
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S')
        log_file = f"{timestamp}_error.log"
        log_path = os.path.join(log_dir, log_file)

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(LogLevel.ERROR.value)

        self.logger.addHandler(file_handler)

    def log(self, level, message):
        # create file handler when first error log come, but don't create more than once
        if level == LogLevel.ERROR.value:
            if not any(isinstance(handler, logging.FileHandler) for handler in self.logger.handlers):
                self._create_file_handler()
        self.logger.log(level.value, message)
