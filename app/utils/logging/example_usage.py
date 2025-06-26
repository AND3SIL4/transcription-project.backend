"""
Example usage of the TranscriptionLogger module in other parts of the project.
This file demonstrates how to use the logging module in different scenarios.
"""

from logger_config import get_logger, default_logger


def example_basic_usage():
    """Example of basic logger usage."""
    # Using the default logger
    default_logger.info("This is a basic info message")
    default_logger.error("This is an error message")

    # Using a custom logger
    custom_logger = get_logger("custom_module")
    custom_logger.info("This is from a custom module")
    custom_logger.warning("This is a warning from custom module")


def example_file_operations():
    """Example of logging file operations."""
    logger = get_logger("file_processor")

    # Log different file operations
    logger.log_file_operation(
        "read", "/path/to/input.txt", "Reading configuration file"
    )
    logger.log_file_operation("write", "/path/to/output.txt", "Writing processed data")
    logger.log_file_operation(
        "delete", "/path/to/temp.txt", "Cleaning up temporary file"
    )


def example_api_requests():
    """Example of logging API requests."""
    logger = get_logger("api_client")

    # Log different API requests
    logger.log_api_request("/users", "GET", "Fetching user list")
    logger.log_api_request("/users/123", "POST", "Creating new user")
    logger.log_api_request("/transcriptions", "PUT", "Updating transcription")


def example_transcription_logging():
    """Example of transcription-specific logging."""
    logger = get_logger("transcription_worker")

    # Log transcription process
    logger.log_transcription_start("video_001.mp4")
    logger.info("Processing video file...")
    logger.log_transcription_success("video_001.mp4", 1500)

    # Log transcription error
    logger.log_transcription_error("video_002.mp4", "Audio file corrupted")


def example_different_log_levels():
    """Example of using different log levels."""
    logger = get_logger("debug_module")

    logger.debug("This is a debug message - only visible if level is DEBUG")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    print("Running logging examples...")

    example_basic_usage()
    example_file_operations()
    example_api_requests()
    example_transcription_logging()
    example_different_log_levels()

    print("Examples completed. Check the logs directory for output files.")
