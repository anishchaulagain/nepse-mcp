"""MACD (Moving Average Convergence Divergence) indicator."""

import pandas as pd


def calculate_ema(series: pd.Series, period: int) -> pd.Series:
    """Calculate Exponential Moving Average."""
    return series.ewm(span=period, adjust=False).mean()


def calculate_macd(
    series: pd.Series,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9,
) -> dict:
    """Calculate MACD line, signal line, and histogram."""
    ema_fast = calculate_ema(series, fast_period)
    ema_slow = calculate_ema(series, slow_period)

    macd_line = ema_fast - ema_slow
    signal_line = calculate_ema(macd_line, signal_period)
    histogram = macd_line - signal_line

    return {
        "macd_line": macd_line,
        "signal_line": signal_line,
        "histogram": histogram,
    }


def get_macd_values(df: pd.DataFrame) -> dict:
    """Calculate MACD and return latest values with trend analysis."""
    result = calculate_macd(df["close"])

    macd_val = float(result["macd_line"].iloc[-1])
    signal_val = float(result["signal_line"].iloc[-1])
    hist_val = float(result["histogram"].iloc[-1])

    # Determine trend from crossover
    prev_hist = float(result["histogram"].iloc[-2]) if len(result["histogram"]) >= 2 else 0

    if hist_val > 0 and prev_hist <= 0:
        trend = "bullish_crossover"
    elif hist_val < 0 and prev_hist >= 0:
        trend = "bearish_crossover"
    elif hist_val > 0:
        trend = "bullish"
    elif hist_val < 0:
        trend = "bearish"
    else:
        trend = "neutral"

    def safe_round(val, places=4):
        if pd.isna(val):
            return None
        return round(float(val), places)

    return {
        "macd_line": safe_round(macd_val, 4),
        "signal_line": safe_round(signal_val, 4),
        "histogram": safe_round(hist_val, 4),
        "trend": trend,
        "macd_series": result["macd_line"],
        "signal_series": result["signal_line"],
        "histogram_series": result["histogram"],
    }
