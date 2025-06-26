import logging
import os
from datetime import datetime
from typing import Optional


class TranscriptionLogger:
    """
    A reusable logging module for the transcription project.
    Provides centralized logging configuration and methods.
    """

    def __init__(self, name: str = "transcription_app", log_dir: str = "logs"):
        """
        Initialize the logger with custom configuration.

        Args:
            name (str): Logger name
            log_dir (str): Directory to store log files
        """
        self.name = name
        self.log_dir = log_dir
        self.logger = None
        self._setup_logger()

    def _setup_logger(self):
        """Setup the logger with file handler and formatter."""
        # Create logs directory if it doesn't exist
        os.makedirs(self.log_dir, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if not self.logger.handlers:
            # Create file handler with date-based filename
            log_filename = f"{self.name}_{datetime.now().strftime('%Y%m%d')}.log"
            log_path = os.path.join(self.log_dir, log_filename)
            handler = logging.FileHandler(log_path, encoding="utf-8")

            # Create formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)

            # Add handler to logger
            self.logger.addHandler(handler)

        # Prevent logs from bubbling up to root logger
        self.logger.propagate = False

        # Disable FastAPI/Uvicorn automatic logs
        self._disable_framework_logs()

    def _disable_framework_logs(self):
        """Disable automatic framework logs to reduce noise."""
        logging.getLogger("uvicorn").setLevel(logging.WARNING)
        logging.getLogger("fastapi").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
        logging.getLogger("uvicorn.error").setLevel(logging.WARNING)

    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)

    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)

    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)

    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)

    def critical(self, message: str):
        """Log a critical message."""
        self.logger.critical(message)

    def log_transcription_start(self, filename: str):
        """Log the start of a transcription process."""
        self.info(f"Starting transcription process for file: {filename}")

    def log_transcription_success(self, filename: str, text_length: int):
        """Log successful transcription completion."""
        self.info(
            f"Transcription completed successfully for {filename}. Text length: {text_length} characters"
        )

    def log_transcription_error(self, filename: str, error: str):
        """Log transcription error."""
        self.error(f"Transcription failed for {filename}: {error}")

    def log_file_operation(
        self, operation: str, filepath: str, details: Optional[str] = None
    ):
        """Log file operations."""
        message = f"File operation '{operation}': {filepath}"
        if details:
            message += f" - {details}"
        self.info(message)

    def log_api_request(
        self, endpoint: str, method: str, details: Optional[str] = None
    ):
        """Log API requests."""
        message = f"API {method} request to {endpoint}"
        if details:
            message += f" - {details}"
        self.info(message)


# Create a default logger instance
default_logger = TranscriptionLogger()


def get_logger(
    name: str = "transcription_app", log_dir: str = "logs"
) -> TranscriptionLogger:
    """
    Get a logger instance with the specified configuration.

    Args:
        name (str): Logger name
        log_dir (str): Directory to store log files

    Returns:
        TranscriptionLogger: Configured logger instance
    """
    return TranscriptionLogger(name, log_dir)


def setup_logging(
    name: str = "transcription_app", log_dir: str = "logs"
) -> TranscriptionLogger:
    """
    Setup and return a logger instance (alias for get_logger for backward compatibility).

    Args:
        name (str): Logger name
        log_dir (str): Directory to store log files

    Returns:
        TranscriptionLogger: Configured logger instance
    """
    return get_logger(name, log_dir)
