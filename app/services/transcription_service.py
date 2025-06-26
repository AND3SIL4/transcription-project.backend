"""
Transcription service for processing video files and generating transcriptions.
"""

import os
import tempfile
from datetime import datetime
from io import BytesIO
from typing import Tuple

from elevenlabs.client import ElevenLabs
from moviepy import VideoFileClip

from app.core.config import settings
from app.utils.logging.logger_config import get_logger

logger = get_logger("transcription_service")


class TranscriptionService:
    """Service for handling video transcription operations."""

    def __init__(self):
        """Initialize the transcription service."""
        self.elevenlabs = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        logger.info("TranscriptionService initialized")

    def process_video(self, video_content: bytes, filename: str) -> Tuple[str, str]:
        """
        Process a video file and generate transcription.

        Args:
            video_content: Raw video file content
            filename: Original filename

        Returns:
            Tuple of (transcription_text, transcription_filename)

        Raises:
            ValueError: If video processing fails
            Exception: For other processing errors
        """
        logger.log_transcription_start(filename)

        # Create temporary files
        temp_video_path = None
        temp_audio_path = None

        try:
            # Save video to temporary file
            temp_video_path = self._save_temp_video(video_content)
            logger.log_file_operation(
                "save", temp_video_path, f"Size: {len(video_content)} bytes"
            )

            # Extract audio from video
            temp_audio_path = self._extract_audio(temp_video_path)

            # Perform transcription
            transcription_text = self._transcribe_audio(temp_audio_path)

            # Save transcription to file
            transcription_filename = self._save_transcription(transcription_text)

            logger.log_transcription_success(filename, len(transcription_text))

            return transcription_text, transcription_filename

        except Exception as e:
            logger.log_transcription_error(filename, str(e))
            raise
        finally:
            # Clean up temporary files
            if temp_video_path:
                self._cleanup_temp_files(temp_video_path)
            if temp_audio_path:
                self._cleanup_temp_files(temp_audio_path)

    def _save_temp_video(self, video_content: bytes) -> str:
        """Save video content to a temporary file."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mkv") as tmp_file:
            tmp_file.write(video_content)
            return tmp_file.name

    def _extract_audio(self, video_path: str) -> str:
        """Extract audio from video file."""
        logger.info("Extracting audio from video file")

        video = VideoFileClip(video_path)
        if video.audio is None:
            video.close()
            raise ValueError("No audio stream found in video")

        logger.info(f"Audio duration: {video.audio.duration} seconds")

        audio_path = video_path + ".mp3"
        logger.log_file_operation("convert", audio_path, "Video to MP3")

        video.audio.write_audiofile(audio_path)
        video.audio.close()
        video.close()

        logger.info("Audio extraction completed successfully")
        return audio_path

    def _transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio using ElevenLabs API."""
        logger.info("Starting ElevenLabs transcription process")

        with open(audio_path, "rb") as audio_file:
            audio_data = BytesIO(audio_file.read())

        logger.info(f"Audio file size: {len(audio_data.getvalue())} bytes")

        # Get ElevenLabs configuration
        config = settings.get_elevenlabs_config()

        transcription = self.elevenlabs.speech_to_text.convert(
            file=audio_data, **config
        )

        logger.info("Transcription completed successfully")
        return transcription.text

    def _save_transcription(self, transcription_text: str) -> str:
        """Save transcription text to a file."""
        transcription_filename = (
            f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        transcription_path = os.path.join(
            settings.TRANSCRIPTIONS_DIR, transcription_filename
        )

        # Ensure directory exists
        os.makedirs(settings.TRANSCRIPTIONS_DIR, exist_ok=True)

        logger.log_file_operation("save", transcription_path, "Transcription result")

        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(transcription_text)

        return transcription_filename

    def _cleanup_temp_files(self, *file_paths: str) -> None:
        """Clean up temporary files."""
        logger.info("Cleaning up temporary files")

        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.info(f"Removed temporary file: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to remove temporary file {file_path}: {e}")

        logger.info("Temporary files cleaned up successfully")

    def get_transcription_file_path(self, filename: str) -> str:
        """Get the full path to a transcription file."""
        return os.path.join(settings.TRANSCRIPTIONS_DIR, filename)

    def transcription_file_exists(self, filename: str) -> bool:
        """Check if a transcription file exists."""
        file_path = self.get_transcription_file_path(filename)
        return os.path.exists(file_path)


# Create service instance
transcription_service = TranscriptionService()
