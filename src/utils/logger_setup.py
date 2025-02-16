import logging
import os
import time
from logging.handlers import RotatingFileHandler
from src.config.settings_reader import get_config

class LoggerSetup:
    def __init__(self):
        self.log_dir = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "logs"
        )
        self.log_file = os.path.join(self.log_dir, "app.log")
        self.max_bytes = 10 * 1024 * 1024  # 10MB
        self.backup_count = 5
        self.project_loggers = {}

        os.makedirs(self.log_dir, exist_ok=True)

        self.logger = self._setup_logging()

    def _setup_logging(self, log_file=None):
        """Global Logger Kurulumu"""
        log_file = log_file or self.log_file

        log_level_str = get_config("log_level", "INFO").upper()
        log_level = getattr(logging, log_level_str, logging.INFO)

        logger = logging.getLogger(log_file)
        logger.setLevel(log_level)

        if logger.hasHandlers():
            logger.handlers.clear()

        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_bytes,
            backupCount=self.backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        return logger

    def _get_project_logger(self, project_name):
        if project_name not in self.project_loggers:
            log_file = os.path.join(self.log_dir, f"{project_name}.log")
            self.project_loggers[project_name] = self._setup_logging(log_file)
        return self.project_loggers[project_name]

    def get_log_file_path(self, project_name):
        """Returns the log file path for the given project name."""
        return os.path.join(self.log_dir, f"{project_name}.log")

    def log_with_project(self, message, repo_path=None, level="info"):
        project_name = os.path.basename(repo_path) if repo_path else "APP"
        logger = self._get_project_logger(project_name) if repo_path else self.logger
        log_message = f"{project_name} | {message}"
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(log_message)

    def read_log_continuously(self, callback, project_name=None):
        log_path = self.log_file
        with open(log_path, "r") as log_file:
            # Dosyanın sonuna git
            log_file.seek(0, os.SEEK_END)
            while True:
                line = log_file.readline()
                if not line:
                    time.sleep(0.1)  # Yeni satır gelene kadar bekle
                    continue
                self.logger.debug(f"Read line: {line.strip()}")
                if project_name and f"{project_name} |" not in line:
                    continue
                callback(line.strip())

logger_setup = LoggerSetup()
global_logger = logger_setup.logger  # Klasik logger çağrılarını destekler
log_with_project = logger_setup.log_with_project  # Proje bazlı log çağrısını destekler
get_log_file = logger_setup.get_log_file_path
