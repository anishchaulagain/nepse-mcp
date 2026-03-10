"""Backtest API routes."""

from fastapi import APIRouter, Query
from app.services.backtest_service import run_backtest

router = APIRouter(tags=["Backtest"])


@router.get("/stocks/{symbol}/backtest")
async def get_backtest(
    symbol: str,
    days: int = Query(180, ge=30, le=500),
    initial_capital: float = Query(100000.0)
):
    """Run a backtest for a stock symbol."""
    return await run_backtest(symbol, initial_capital, days)
