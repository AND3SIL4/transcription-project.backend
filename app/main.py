"""
Main FastAPI application for the transcript recordings backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import router
from app.core.config import settings
from app.utils.logging.logger_config import get_logger

# Initialize logger
logger = get_logger("main_app")

# Validate configuration
try:
    settings.validate_config()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="A FastAPI-based backend service for transcribing video recordings using ElevenLabs' speech-to-text API.",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router, prefix=settings.API_V1_STR)

    # Add root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Transcript Recordings Backend API",
            "version": settings.VERSION,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    # Add health check endpoint
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": settings.PROJECT_NAME}

    logger.info("FastAPI application created successfully")
    return app


# Create application instance
app = create_app()

# Log application startup
logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
logger.info("FastAPI application started successfully")
