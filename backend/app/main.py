"""NEPSE AI Prediction Platform — FastAPI Application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import get_settings
from app.api.routes import stocks, indicators, prediction, ai_analysis, backtest
from app.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    settings = get_settings()
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    yield
    logger.info("Shutting down...")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered NEPSE stock analysis and prediction platform",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API routers
    prefix = settings.API_V1_PREFIX
    app.include_router(stocks.router, prefix=prefix)
    app.include_router(indicators.router, prefix=prefix)
    app.include_router(prediction.router, prefix=prefix)
    app.include_router(ai_analysis.router, prefix=prefix)
    app.include_router(backtest.router, prefix=prefix)

    @app.get("/")
    async def root():
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs",
        }

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


app = create_app()
