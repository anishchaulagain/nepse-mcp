"""Dependency injection for API routes."""

from app.config.settings import get_settings, Settings


def get_app_settings() -> Settings:
    return get_settings()
