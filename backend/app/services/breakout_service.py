"""Breakout detection service."""

import pandas as pd
import numpy as np
from app.services.nepse_service import get_stock_candles
from app.core.indicators.bollinger import get_bollinger_values
from app.core.prediction_engine import detect_volume_spike
from app.schemas.prediction_schema import BreakoutResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


def detect_resistance_break(df: pd.DataFrame, lookback: int = 20) -> dict:
    """Detect if price broke above recent resistance."""
    recent_highs = df["high"].iloc[-lookback:-1]
    resistance = float(recent_highs.max())
    current = float(df["close"].iloc[-1])

    return {
        "broken": current > resistance,
        "resistance": round(resistance, 2),
        "current": round(current, 2),
    }


def detect_support_break(df: pd.DataFrame, lookback: int = 20) -> dict:
    """Detect if price broke below recent support."""
    recent_lows = df["low"].iloc[-lookback:-1]
    support = float(recent_lows.min())
    current = float(df["close"].iloc[-1])

    return {
        "broken": current < support,
        "support": round(support, 2),
        "current": round(current, 2),
    }


async def detect_breakout(symbol: str) -> BreakoutResponse:
    """Detect breakout using resistance break, volume spike, and Bollinger squeeze."""
    logger.info(f"Detecting breakout for {symbol}")
    df = await get_stock_candles(symbol)

    resistance = detect_resistance_break(df)
    support = detect_support_break(df)
    bollinger = get_bollinger_values(df)
    volume = detect_volume_spike(df)

    reasons = []
    breakout_score = 0

    # Bullish breakout signals
    if resistance["broken"]:
        breakout_score += 2
        reasons.append(f"Price broke resistance at {resistance['resistance']}")

    if volume["spike"]:
        breakout_score += 1
        reasons.append(f"Volume spike: {volume['ratio']}x average")

    if bollinger["squeeze"]:
        breakout_score += 1
        reasons.append("Bollinger Band squeeze detected")

    # Bearish breakout signals
    bearish_score = 0
    if support["broken"]:
        bearish_score += 2
        reasons.append(f"Price broke support at {support['support']}")

    if volume["spike"] and support["broken"]:
        bearish_score += 1

    # Determine breakout
    is_breakout = breakout_score >= 2 or bearish_score >= 2
    breakout_type = "none"

    if breakout_score >= 2 and breakout_score > bearish_score:
        breakout_type = "bullish"
    elif bearish_score >= 2:
        breakout_type = "bearish"

    confidence = min((max(breakout_score, bearish_score) / 4), 0.95) if is_breakout else 0.1

    return BreakoutResponse(
        symbol=symbol.upper(),
        breakout=is_breakout,
        type=breakout_type,
        confidence=round(confidence, 2),
        reasons=reasons,
    )
