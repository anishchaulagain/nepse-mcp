"""NEPSE data service — fetches/generates OHLCV data for stocks."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Fallback base prices for common stocks (optional context, but not a fixed list)
BASE_PRICES = {
    "NABIL": 350, "NICA": 280, "GBIME": 240, "NTC": 600, "SHIVM": 340
}


def generate_mock_ohlcv(symbol: str, days: int = 365) -> pd.DataFrame:
    """Generate realistic mock OHLCV data for a given stock."""
    symbol = symbol.upper()
    base_price = BASE_PRICES.get(symbol, 300)

    np.random.seed(hash(symbol) % 2**32)

    dates = pd.date_range(end=datetime.now(), periods=days, freq="B")  # business days

    # Generate realistic price movement using geometric Brownian motion
    drift = 0.0002
    volatility = 0.018
    dt = 1.0

    returns = np.random.normal(drift, volatility, days)
    prices = base_price * np.exp(np.cumsum(returns))

    # Add some trend patterns
    trend = np.sin(np.linspace(0, 4 * np.pi, days)) * base_price * 0.08
    prices = prices + trend

    # Generate OHLCV
    opens = prices * (1 + np.random.uniform(-0.005, 0.005, days))
    highs = np.maximum(prices, opens) * (1 + np.random.uniform(0.002, 0.02, days))
    lows = np.minimum(prices, opens) * (1 - np.random.uniform(0.002, 0.02, days))

    base_volume = np.random.randint(50000, 200000, days).astype(float)
    # Add volume spikes
    spike_mask = np.random.random(days) > 0.92
    base_volume[spike_mask] *= np.random.uniform(2.0, 4.0, spike_mask.sum())

    df = pd.DataFrame({
        "timestamp": dates,
        "open": np.round(opens, 2),
        "high": np.round(highs, 2),
        "low": np.round(lows, 2),
        "close": np.round(prices, 2),
        "volume": base_volume.astype(int),
        "amount": np.round(prices * base_volume, 2),
    })

    return df


from app.services.api_adapters import fetch_chukul_data, fetch_nepalipaisa_data

async def get_stock_candles(symbol: str, timeframe: str = "1D", days: int = 365) -> pd.DataFrame:
    """Get OHLCV candles for a symbol. Tries real data, falls back to mock."""
    logger.info(f"Fetching real candles for {symbol}, timeframe={timeframe}")
    
    # Try fetching real data from Chukul (Only 1D supported for now)
    if timeframe.upper() == "1D":
        real_df = await fetch_chukul_data(symbol, days)
        if real_df is not None and not real_df.empty:
            logger.info(f"Successfully fetched real data for {symbol} from Chukul")
            return real_df

    logger.warning(f"Could not fetch real data for {symbol}, falling back to mock")
    return generate_mock_ohlcv(symbol.upper(), days)


async def get_stock_list() -> list[dict]:
    """Get list of recent/trending stocks (now empty since we use search)."""
    # In a real app, this could fetch from a cache or a dynamic discovery API
    # For now, we return an empty list to indicate search is expected
    return []
