"""
API endpoints for the transcript recordings backend.
"""

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.services.transcription_service import transcription_service
from app.utils.logging.logger_config import get_logger

logger = get_logger("api_endpoints")

router = APIRouter()


@router.post("/transcribe")
async def transcribe_video(file: UploadFile = File(...)):
    """
    Transcribe a video file to text.

    Args:
        file: Video file to transcribe

    Returns:
        JSON response with transcription status and filename
    """
    filename = file.filename or "unknown_file"
    logger.log_api_request("/transcribe", "POST", f"File: {filename}")

    try:
        # Validate file type
        logger.info(f"Validating file type: {file.content_type}")
        if not (file.content_type and file.content_type.startswith("video/")):
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(
                status_code=400,
                detail=f"File must be a video. Received: {file.content_type}",
            )

        # Check file size
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            logger.error(f"File too large: {len(content)} bytes")
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE} bytes",
            )

        # Process video and generate transcription
        transcription_text, transcription_filename = (
            transcription_service.process_video(content, filename)
        )

        logger.info(
            f"Transcription process completed successfully. File: {transcription_filename}"
        )

        return {
            "message": "Transcription completed successfully",
            "transcription_file": transcription_filename,
            "text_length": len(transcription_text),
        }

    except ValueError as e:
        logger.error(f"Validation error for {filename}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error processing {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")


@router.get("/download-transcription/{filename}")
async def download_transcription(filename: str):
    """
    Download a transcription file.

    Args:
        filename: Name of the transcription file to download

    Returns:
        File response with the transcription content
    """
    logger.log_api_request(
        "/download-transcription/{filename}", "GET", f"File: {filename}"
    )

    try:
        # Validate filename
        if not filename or ".." in filename or "/" in filename:
            raise HTTPException(status_code=400, detail="Invalid filename")

        # Check if file exists
        if not transcription_service.transcription_file_exists(filename):
            logger.error(f"Transcription file not found: {filename}")
            raise HTTPException(status_code=404, detail="Transcription file not found")

        # Get file path and serve file
        file_path = transcription_service.get_transcription_file_path(filename)
        logger.log_file_operation("download", file_path, "File served successfully")

        return FileResponse(file_path, filename=filename)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error serving file")
