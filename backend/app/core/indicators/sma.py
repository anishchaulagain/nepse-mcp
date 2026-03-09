"""Simple Moving Average indicator."""

import pandas as pd


def calculate_sma(series: pd.Series, period: int) -> pd.Series:
    """Calculate Simple Moving Average for a given period."""
    return series.rolling(window=period, min_periods=1).mean()


def get_sma_values(df: pd.DataFrame) -> dict:
    """Calculate SMA 20, 50, 200 and return latest values."""
    close = df["close"]

    sma20 = calculate_sma(close, 20)
    sma50 = calculate_sma(close, 50)
    sma200 = calculate_sma(close, 200)

    return {
        "sma20": round(float(sma20.iloc[-1]), 2) if len(sma20) > 0 else None,
        "sma50": round(float(sma50.iloc[-1]), 2) if len(sma50) > 0 else None,
        "sma200": round(float(sma200.iloc[-1]), 2) if len(sma200) > 0 else None,
        "sma20_series": sma20,
        "sma50_series": sma50,
        "sma200_series": sma200,
    }
