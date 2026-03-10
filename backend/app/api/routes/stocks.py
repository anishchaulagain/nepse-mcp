"""Stock API routes — candle data and stock listing."""

from fastapi import APIRouter, Query

from app.services.nepse_service import get_stock_candles, get_stock_list

router = APIRouter(tags=["Stocks"])


@router.get("/stocks")
async def list_stocks():
    """List all available NEPSE stocks with latest prices."""
    stocks = await get_stock_list()
    return {"stocks": stocks, "total": len(stocks)}


@router.get("/stocks/{symbol}/candles")
async def get_candles(
    symbol: str,
    timeframe: str = Query("1D", description="Candle timeframe"),
    days: int = Query(365, ge=30, le=1000, description="Number of days"),
):
    """Get OHLCV candle data for a stock."""
    df = await get_stock_candles(symbol, timeframe, days)

    candles = []
    for _, row in df.iterrows():
        candles.append({
            "time": row["timestamp"].strftime("%Y-%m-%d"),
            "open": round(float(row["open"]), 2),
            "high": round(float(row["high"]), 2),
            "low": round(float(row["low"]), 2),
            "close": round(float(row["close"]), 2),
            "volume": int(row["volume"]),
        })

    return {
        "symbol": symbol.upper(),
        "timeframe": timeframe,
        "candles": candles,
        "total": len(candles),
    }
