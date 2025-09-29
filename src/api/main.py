"""
Main FastAPI application module.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core import router as api_router
from ..utils.config import Config

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title=Config.APP_NAME,
        description=Config.APP_DESCRIPTION,
        version=Config.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=Config.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers
    app.include_router(api_router, prefix="/api")

    return app

# Create the FastAPI application instance
app = create_app()
