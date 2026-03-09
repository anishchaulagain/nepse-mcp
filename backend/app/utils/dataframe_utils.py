"""Utilities for converting raw NEPSE JSON data to Pandas DataFrames."""

import pandas as pd
import numpy as np
from typing import Any


def ohlcv_json_to_dataframe(data: dict[str, list]) -> pd.DataFrame:
    """Convert raw OHLCV JSON (t, o, h, l, c, vol, amt) to a DataFrame.

    Input format:
        {"t": [...], "o": [...], "c": [...], "h": [...], "l": [...], "vol": [...], "amt": [...]}
    """
    df = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(data["t"], unit="ms"),
            "open": pd.to_numeric(data["o"], errors="coerce"),
            "high": pd.to_numeric(data["h"], errors="coerce"),
            "low": pd.to_numeric(data["l"], errors="coerce"),
            "close": pd.to_numeric(data["c"], errors="coerce"),
            "volume": pd.to_numeric(data["vol"], errors="coerce"),
            "amount": pd.to_numeric(data.get("amt", [0] * len(data["t"])), errors="coerce"),
        }
    )
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


def price_history_to_dataframe(results: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert price history API response to DataFrame.

    Input format:
        [{"tradeDate": 1773014400000, "closingPrice": 364.10}, ...]
    """
    df = pd.DataFrame(results)
    df["timestamp"] = pd.to_datetime(df["tradeDate"], unit="ms")
    df["close"] = pd.to_numeric(df["closingPrice"], errors="coerce")
    df = df[["timestamp", "close"]].sort_values("timestamp").reset_index(drop=True)
    return df
