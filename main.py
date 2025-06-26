from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from moviepy import VideoFileClip
import os
import tempfile
from io import BytesIO
from datetime import datetime
from logging.logger_config import get_logger

# Initialize logger
logger = get_logger("transcription_app")

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# Initialize ElevenLabs client
elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
logger.info("ElevenLabs client initialized")

logger.info("FastAPI application started successfully")


@app.post("/transcribe")
async def transcribe_video(file: UploadFile = File(...)):
    filename = file.filename or "unknown_file"
    logger.log_transcription_start(filename)
    logger.log_api_request("/transcribe", "POST", f"File: {filename}")

    try:
        # Validate file type
        logger.info(f"Validating file type: {file.content_type}")
        if not (file.content_type and file.content_type.startswith("video/")):
            logger.error(f"Invalid file type: {file.content_type}")
            raise HTTPException(status_code=400, detail="File must be a video")

        # Save uploaded video temporarily
        logger.info("Saving uploaded video to temporary file")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mkv") as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name
        logger.log_file_operation("save", tmp_file_path, f"Size: {len(content)} bytes")

        # Extract audio from video
        logger.info("Extracting audio from video file")
        video = VideoFileClip(tmp_file_path)
        if video.audio is None:
            logger.error("No audio stream found in video file")
            video.close()
            os.remove(tmp_file_path)
            raise HTTPException(
                status_code=400, detail="No audio stream found in video"
            )

        logger.info(f"Audio duration: {video.audio.duration} seconds")
        audio_path = tmp_file_path + ".mp3"
        logger.log_file_operation("convert", audio_path, "Video to MP3")
        video.audio.write_audiofile(audio_path)
        video.audio.close()
        video.close()
        logger.info("Audio extraction completed successfully")

        # Read audio into BytesIO
        logger.info("Reading audio file into memory")
        with open(audio_path, "rb") as audio_file:
            audio_data = BytesIO(audio_file.read())
        logger.info(f"Audio file size: {len(audio_data.getvalue())} bytes")

        # Perform transcription
        logger.info("Starting ElevenLabs transcription process")
        transcription = elevenlabs.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1",
            tag_audio_events=True,
            language_code="es",
            diarize=True,
        )
        logger.info("Transcription completed successfully")

        # Save transcription to a file with unique filename
        transcription_filename = (
            f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        transcription_path = os.path.join("transcriptions", transcription_filename)
        os.makedirs("transcriptions", exist_ok=True)  # Ensure directory exists
        logger.log_file_operation("save", transcription_path, "Transcription result")
        with open(transcription_path, "w", encoding="utf-8") as f:
            f.write(transcription.text)
        logger.log_transcription_success(
            transcription_filename, len(transcription.text)
        )

        # Clean up temporary files
        logger.info("Cleaning up temporary files")
        os.remove(tmp_file_path)
        os.remove(audio_path)
        logger.info("Temporary files cleaned up successfully")

        # Log and return short success message
        logger.info(
            f"Transcription process completed successfully. File: {transcription_filename}"
        )
        return {
            "message": "Transcription completed successfully",
            "transcription_file": transcription_filename,
        }

    except Exception as e:
        logger.log_transcription_error(filename, str(e))
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")


@app.get("/download-transcription/{filename}")
async def download_transcription(filename: str):
    logger.log_api_request(
        "/download-transcription/{filename}", "GET", f"File: {filename}"
    )
    transcription_path = os.path.join("transcriptions", filename)
    if os.path.exists(transcription_path):
        logger.log_file_operation(
            "download", transcription_path, "File served successfully"
        )
        return FileResponse(transcription_path, filename=filename)
    logger.error(f"Transcription file not found: {filename}")
    raise HTTPException(status_code=404, detail="Transcription file not found")
