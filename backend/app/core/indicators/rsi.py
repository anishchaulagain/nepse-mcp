"""Relative Strength Index (RSI) indicator."""

import pandas as pd
import numpy as np


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculate RSI using Wilder's smoothing method."""
    if len(series) <= period:
        return pd.Series(np.nan, index=series.index)

    delta = series.diff()

    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)

    # First average: simple mean of first `period` values
    avg_gain = gain.copy()
    avg_loss = loss.copy()

    avg_gain.iloc[:period] = np.nan
    avg_loss.iloc[:period] = np.nan

    first_avg_gain = gain.iloc[1 : period + 1].mean()
    first_avg_loss = loss.iloc[1 : period + 1].mean()

    avg_gain.iloc[period] = first_avg_gain
    avg_loss.iloc[period] = first_avg_loss

    # Wilder's smoothing
    for i in range(period + 1, len(series)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def get_rsi_value(df: pd.DataFrame, period: int = 14) -> dict:
    """Calculate RSI and return the latest value."""
    rsi = calculate_rsi(df["close"], period)
    latest = float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None

    status = "neutral"
    if latest is not None:
        if latest >= 70:
            status = "overbought"
        elif latest <= 30:
            status = "oversold"
        elif latest >= 60:
            status = "bullish"
        elif latest <= 40:
            status = "bearish"

    return {
        "value": round(latest, 2) if latest is not None else None,
        "status": status,
        "series": rsi,
    }
