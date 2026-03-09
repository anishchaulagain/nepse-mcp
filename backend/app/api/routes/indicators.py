"""Indicator API routes."""

from fastapi import APIRouter

from app.services.indicator_service import calculate_indicators, get_indicator_series

router = APIRouter(tags=["Indicators"])


@router.get("/stocks/{symbol}/indicators")
async def get_indicators(symbol: str):
    """Get all technical indicators for a stock."""
    result = calculate_indicators(symbol)
    return result.model_dump()


@router.get("/stocks/{symbol}/indicators/series")
async def get_indicator_time_series(symbol: str):
    """Get indicator time series data for charting."""
    return get_indicator_series(symbol)
