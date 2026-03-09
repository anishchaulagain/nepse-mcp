"""Bollinger Bands indicator."""

import pandas as pd


def calculate_bollinger_bands(
    series: pd.Series, period: int = 20, std_dev: float = 2.0
) -> dict:
    """Calculate Bollinger Bands (upper, middle, lower)."""
    middle = series.rolling(window=period, min_periods=1).mean()
    std = series.rolling(window=period, min_periods=1).std()

    upper = middle + (std * std_dev)
    lower = middle - (std * std_dev)

    return {"upper": upper, "middle": middle, "lower": lower, "std": std}


def get_bollinger_values(df: pd.DataFrame) -> dict:
    """Calculate Bollinger Bands and return latest values."""
    bands = calculate_bollinger_bands(df["close"])

    upper = float(bands["upper"].iloc[-1])
    middle = float(bands["middle"].iloc[-1])
    lower = float(bands["lower"].iloc[-1])

    # Bandwidth = (upper - lower) / middle * 100
    bandwidth = ((upper - lower) / middle * 100) if middle != 0 else 0

    current_price = float(df["close"].iloc[-1])

    # Position within bands (0 = at lower, 1 = at upper)
    band_position = (
        (current_price - lower) / (upper - lower) if (upper - lower) != 0 else 0.5
    )

    # Squeeze detection: bandwidth < threshold (typically < 4%)
    squeeze = bandwidth < 4.0

    return {
        "upper": round(upper, 2),
        "middle": round(middle, 2),
        "lower": round(lower, 2),
        "bandwidth": round(bandwidth, 4),
        "band_position": round(band_position, 4),
        "squeeze": squeeze,
        "upper_series": bands["upper"],
        "middle_series": bands["middle"],
        "lower_series": bands["lower"],
    }
