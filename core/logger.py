import logging
import os
from logging.handlers import RotatingFileHandler


class Logger:

    @staticmethod
    def get_logger(name="Automation", log_file="automation.log", level=logging.INFO):
        """
        Returns a logger that writes to both console and file.
        """

        # Create logs directory if not exists
        os.makedirs("logs", exist_ok=True)
        log_path = os.path.join("logs", log_file)

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Avoid duplicate handlers if logger already created
        if logger.handlers:
            return logger

        # ------------------------------
        # FORMATTER
        # ------------------------------
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # ------------------------------
        # FILE HANDLER (Rotating)
        # ------------------------------
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=2 * 1024 * 1024,  # 2 MB
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        # ------------------------------
        # CONSOLE HANDLER
        # ------------------------------
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
