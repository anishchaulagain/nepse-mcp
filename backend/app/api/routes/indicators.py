"""Indicator API routes."""

from fastapi import APIRouter

from app.services.indicator_service import calculate_indicators, get_indicator_series

router = APIRouter(tags=["Indicators"])


@router.get("/stocks/{symbol}/indicators")
async def get_indicators(symbol: str):
    """Get all technical indicators for a stock."""
    return await calculate_indicators(symbol)


@router.get("/stocks/{symbol}/indicators/series")
async def get_indicators_series(symbol: str):
    """Get indicator time series for charting."""
    return await get_indicator_series(symbol)
