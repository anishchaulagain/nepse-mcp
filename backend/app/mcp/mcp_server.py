"""MCP (Model Context Protocol) server for NEPSE AI tools."""

from mcp.server.fastmcp import FastMCP

from app.services.nepse_service import get_stock_candles
from app.services.indicator_service import calculate_indicators
from app.services.prediction_service import predict_trend
from app.services.breakout_service import detect_breakout

mcp = FastMCP("NEPSE AI Analyst")


@mcp.tool()
def get_stock_candles_tool(symbol: str, timeframe: str = "1D") -> dict:
    """Get OHLCV candle data for a NEPSE stock.

    Args:
        symbol: Stock ticker symbol (e.g. NABIL, NICA, SBL)
        timeframe: Candle timeframe (default: 1D)
    """
    df = get_stock_candles(symbol, timeframe)
    candles = []
    for _, row in df.tail(30).iterrows():
        candles.append({
            "time": row["timestamp"].strftime("%Y-%m-%d"),
            "open": round(float(row["open"]), 2),
            "high": round(float(row["high"]), 2),
            "low": round(float(row["low"]), 2),
            "close": round(float(row["close"]), 2),
            "volume": int(row["volume"]),
        })
    return {"symbol": symbol.upper(), "candles": candles}


@mcp.tool()
def calculate_indicators_tool(symbol: str) -> dict:
    """Calculate technical indicators for a NEPSE stock.

    Returns RSI, SMA (20/50/200), MACD, Bollinger Bands, and volume analysis.

    Args:
        symbol: Stock ticker symbol (e.g. NABIL)
    """
    result = calculate_indicators(symbol)
    return result.model_dump()


@mcp.tool()
def predict_trend_tool(symbol: str) -> dict:
    """Predict the trend for a NEPSE stock using rule-based AI.

    Returns trend direction, confidence score, and signal details.

    Args:
        symbol: Stock ticker symbol (e.g. NABIL)
    """
    result = predict_trend(symbol)
    return result.model_dump()


@mcp.tool()
def detect_breakout_tool(symbol: str) -> dict:
    """Detect potential breakout signals for a NEPSE stock.

    Analyzes resistance breaks, volume spikes, and Bollinger squeezes.

    Args:
        symbol: Stock ticker symbol (e.g. NABIL)
    """
    result = detect_breakout(symbol)
    return result.model_dump()


@mcp.tool()
def analyze_stock_tool(symbol: str) -> dict:
    """Perform full AI analysis on a NEPSE stock.

    Returns indicators, prediction, breakout detection, and summary.

    Args:
        symbol: Stock ticker symbol (e.g. NABIL)
    """
    indicators = calculate_indicators(symbol)
    prediction = predict_trend(symbol)
    breakout = detect_breakout(symbol)

    df = get_stock_candles(symbol)
    current_price = round(float(df["close"].iloc[-1]), 2)

    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "indicators": indicators.model_dump(),
        "prediction": prediction.model_dump(),
        "breakout": breakout.model_dump(),
    }
