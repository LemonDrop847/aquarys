"""Main FastAPI application for AQUARYS."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aquarys.core.config import settings
from aquarys.core.database import init_db
from aquarys.core.logging import logger, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan events for startup and shutdown."""
    setup_logging()
    logger.info("Starting AQUARYS backend service (mode: %s)...", settings.APP_MODE)
    await init_db()
    logger.info("Database schemas initialized.")
    yield
    logger.info("Shutting down AQUARYS backend service...")


app = FastAPI(
    title="AQUARYS API",
    description="Trust-aware environmental intelligence system for urban streams",
    version=settings.VERSION,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
    }
