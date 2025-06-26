# Transcript Recordings Backend

A FastAPI-based backend service for transcribing video recordings using ElevenLabs' speech-to-text API. This service extracts audio from video files and generates accurate transcriptions with speaker diarization support.

## 🚀 Features

- **Video Processing**: Extract audio from various video formats
- **Speech-to-Text**: High-quality transcription using ElevenLabs API
- **Speaker Diarization**: Identify and separate different speakers in recordings
- **Multi-language Support**: Currently configured for Spanish (easily configurable)
- **File Management**: Automatic transcription file storage and download
- **Comprehensive Logging**: Detailed logging system for monitoring and debugging
- **CORS Support**: Ready for frontend integration
- **Error Handling**: Robust error handling with detailed error messages
- **Modular Architecture**: Clean, maintainable code structure

## 🛠️ Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **ElevenLabs** - Advanced speech-to-text API with diarization
- **MoviePy** - Video processing and audio extraction
- **Python 3.13+** - Latest Python features and performance
- **uv** - Fast Python package manager

## 📋 Prerequisites

- Python 3.13 or higher
- ElevenLabs API key
- Sufficient disk space for temporary video/audio processing

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd backend
```

### 2. Install Dependencies

This project uses `uv` for dependency management:

```bash
# Install uv if you haven't already
pip install uv

# Install project dependencies
uv sync
```

### 3. Environment Setup

Create a `.env` file in the project root:

```env
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

### 4. Run the Application

```bash
# Development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Endpoints

#### POST `/api/v1/transcribe`

Transcribe a video file to text.

**Request:**

- Content-Type: `multipart/form-data`
- Body: Video file upload

**Response:**

```json
{
  "message": "Transcription completed successfully",
  "transcription_file": "transcription_20241201_143022.txt",
  "text_length": 1500
}
```

**Example using curl:**

```bash
curl -X POST "http://localhost:8000/api/v1/transcribe" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_video.mp4"
```

#### GET `/api/v1/download-transcription/{filename}`

Download a transcription file.

**Parameters:**

- `filename`: Name of the transcription file

**Response:**

- File download (text/plain)

**Example:**

```bash
curl -O "http://localhost:8000/api/v1/download-transcription/transcription_20241201_143022.txt"
```

#### GET `/`

Root endpoint with API information.

**Response:**

```json
{
  "message": "Transcript Recordings Backend API",
  "version": "0.1.0",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

#### GET `/health`

Health check endpoint.

**Response:**

```json
{
  "status": "healthy",
  "service": "Transcript Recordings Backend"
}
```

### Interactive API Documentation

Once the server is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📁 Project Structure

```
backend/
├── app/                    # Main application package
│   ├── __init__.py        # App package initialization
│   ├── main.py            # FastAPI application factory
│   ├── api/               # API layer
│   │   ├── __init__.py
│   │   └── endpoints.py   # API route definitions
│   ├── core/              # Core configuration
│   │   ├── __init__.py
│   │   └── config.py      # Application settings
│   ├── services/          # Business logic layer
│   │   ├── __init__.py
│   │   └── transcription_service.py  # Transcription business logic
│   └── utils/             # Utilities and helpers
│       ├── __init__.py
│       └── logging/       # Logging system
│           ├── __init__.py
│           ├── logger_config.py
│           ├── example_usage.py
│           └── LOGGING_README.md
├── main.py                # Application entry point
├── pyproject.toml         # Project configuration and dependencies
├── uv.lock               # Locked dependency versions
├── README.md             # This file
├── .env                  # Environment variables (create this)
├── logs/                 # Generated log files
└── transcriptions/       # Generated transcription files
```

## 🔧 Configuration

### Environment Variables

| Variable             | Description             | Required |
| -------------------- | ----------------------- | -------- |
| `ELEVENLABS_API_KEY` | Your ElevenLabs API key | Yes      |

### Application Settings

The application uses a centralized configuration system in `app/core/config.py`:

- **API Configuration**: Version, project name, CORS settings
- **ElevenLabs Configuration**: API key, model, language settings
- **File Processing**: Maximum file size, allowed video types
- **Storage**: Directories for logs and transcriptions

### ElevenLabs Configuration

The service is configured to use:

- **Model**: `scribe_v1` (high-quality transcription)
- **Language**: Spanish (`es`)
- **Features**:
  - Audio event tagging
  - Speaker diarization
  - Automatic language detection

To change the language, modify the `ELEVENLABS_LANGUAGE_CODE` in `app/core/config.py`:

```python
ELEVENLABS_LANGUAGE_CODE: str = "en"  # Change to desired language code
```

## 📊 Logging System

The project includes a comprehensive logging system with:

- **Date-based log files** in the `logs/` directory
- **Specialized logging methods** for transcriptions, file operations, and API requests
- **Automatic log rotation** by date
- **Framework log suppression** to reduce noise

### Usage Examples

```python
from app.utils.logging.logger_config import get_logger

# Create a logger
logger = get_logger("my_module")

# Basic logging
logger.info("Processing started")
logger.error("An error occurred")

# Specialized logging
logger.log_transcription_start("video.mp4")
logger.log_transcription_success("video.mp4", 1500)
logger.log_file_operation("save", "/path/to/file", "Saving transcription")
logger.log_api_request("/transcribe", "POST", "File: video.mp4")
```

For detailed logging documentation, see `app/utils/logging/LOGGING_README.md`.

## 🏗️ Architecture

The application follows a clean, modular architecture:

- **API Layer** (`app/api/`): Handles HTTP requests and responses
- **Service Layer** (`app/services/`): Contains business logic
- **Core Layer** (`app/core/`): Configuration and shared utilities
- **Utils Layer** (`app/utils/`): Helper functions and logging

This separation of concerns makes the code:

- **Maintainable**: Easy to modify and extend
- **Testable**: Each layer can be tested independently
- **Scalable**: New features can be added without affecting existing code

## 🔒 Security Considerations

- **CORS**: Currently configured to allow all origins (`*`). For production, specify allowed origins.
- **File Validation**: Only video files are accepted with size limits
- **Temporary Files**: All temporary files are automatically cleaned up
- **API Key**: Store your ElevenLabs API key securely in environment variables
- **Input Validation**: Filename validation to prevent path traversal attacks

### Production Recommendations

1. **CORS Configuration**: Update CORS settings to allow only your frontend domain
2. **Rate Limiting**: Implement rate limiting for API endpoints
3. **File Size Limits**: Configure appropriate file size limits
4. **Authentication**: Add authentication/authorization if needed
5. **HTTPS**: Use HTTPS in production
6. **Environment Variables**: Use secure environment variable management

## 🐛 Troubleshooting

### Common Issues

**1. "No audio stream found in video"**

- Ensure your video file contains an audio track
- Try converting the video to a different format

**2. "Invalid file type"**

- Only video files are supported
- Check that the file has a valid video MIME type

**3. "ElevenLabs API error"**

- Verify your API key is correct
- Check your ElevenLabs account balance/limits
- Ensure the audio file is not corrupted

**4. "Permission denied" errors**

- Ensure the application has write permissions to the `logs/` and `transcriptions/` directories

**5. "Configuration error"**

- Check that the `ELEVENLABS_API_KEY` environment variable is set
- Verify the `.env` file is in the correct location

### Debug Mode

To enable debug logging, modify `app/utils/logging/logger_config.py`:

```python
self.logger.setLevel(logging.DEBUG)
```

## 🧪 Development

### Code Quality

The project includes development tools for code quality:

```bash
# Install development dependencies
uv sync --extra dev

# Format code
black app/
isort app/

# Lint code
flake8 app/

# Run tests (when implemented)
pytest
```

### Adding New Features

1. **API Endpoints**: Add new routes in `app/api/endpoints.py`
2. **Business Logic**: Create new services in `app/services/`
3. **Configuration**: Add new settings in `app/core/config.py`
4. **Utilities**: Add helper functions in `app/utils/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [ElevenLabs](https://elevenlabs.io/) for their excellent speech-to-text API
- [FastAPI](https://fastapi.tiangolo.com/) for the modern web framework
- [MoviePy](https://zulko.github.io/moviepy/) for video processing capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the logs in the `logs/` directory
3. Open an issue on GitHub with detailed information about the problem

---

**Note**: This backend is designed to work with a frontend application. Make sure your frontend is configured to communicate with the correct API endpoints and handle the responses appropriately.
