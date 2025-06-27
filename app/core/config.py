"""
Core configuration settings for the application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings and configuration."""

    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Transcript Recordings Backend"
    VERSION: str = "0.1.0"

    # ElevenLabs Configuration
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")
    ELEVENLABS_MODEL_ID: str = "scribe_v1"
    ELEVENLABS_LANGUAGE_CODE: str = "es"

    # File Processing Configuration
    MAX_FILE_SIZE: int = 2 * 1024 * 1024 * 1024  # 2GB
    # MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_TYPES: list = [
        "video/mp4",
        "video/avi",
        "video/mov",
        "video/mkv",
        "video/webm",
        "video/flv",
    ]

    # Storage Configuration
    TRANSCRIPTIONS_DIR: str = "transcriptions"
    LOGS_DIR: str = "logs"

    # CORS Configuration
    CORS_ORIGINS: list = ["*"]  # Configure for production

    @classmethod
    def validate_config(cls) -> None:
        """Validate that all required configuration is present."""
        if not cls.ELEVENLABS_API_KEY:
            raise ValueError("ELEVENLABS_API_KEY environment variable is required")

    @classmethod
    def get_elevenlabs_config(cls) -> dict:
        """Get ElevenLabs API configuration."""
        return {
            "model_id": cls.ELEVENLABS_MODEL_ID,
            "language_code": cls.ELEVENLABS_LANGUAGE_CODE,
            "tag_audio_events": True,
            "diarize": True,
        }


# Create settings instance
settings = Settings()
