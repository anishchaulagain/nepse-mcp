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

    dates = pd.date_range(end=datetime.now(), periods=days, freq="D")  # calendar days for deterministic length

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


from app.services.api_adapters import fetch_chukul_data, fetch_nepalipaisa_data, fetch_chukul_symbols, fetch_nepalipaisa_live_stocks

async def get_stock_candles(symbol: str, timeframe: str = "1D", days: int = 365) -> pd.DataFrame:
    """Get OHLCV candles for a symbol. Tries real data, falls back to mock."""
    logger.info(f"Fetching real candles for {symbol}, timeframe={timeframe}")
    
    # Try fetching real data from Chukul (Only 1D supported for now)
    if timeframe.upper() == "1D":
        real_df = await fetch_chukul_data(symbol, days)
        if real_df is not None and not real_df.empty:
            logger.info(f"Successfully fetched real data for {symbol} from Chukul")
            return real_df.sort_values("timestamp")

    logger.warning(f"Could not fetch real data for {symbol}, falling back to mock")
    df = generate_mock_ohlcv(symbol.upper(), days)
    return df.sort_values("timestamp")


async def get_stock_list() -> list[dict]:
    """Get list of NEPSE stocks from Nepali Paisa API."""
    try:
        raw_stocks = await fetch_nepalipaisa_live_stocks()
        formatted_list = []
        for s in raw_stocks:
            symbol = s.get("stockSymbol", "")
            if not symbol:
                continue
                
            formatted_list.append({
                "symbol": symbol,
                "name": s.get("companyName", ""),
                "sector": "Equity",  # Generic since sector_id is numeric
                "last_price": s.get("closingPrice", 0) or 0,
                "change": s.get("differenceRs", 0) or 0,
                "change_percent": s.get("percentChange", 0) or 0,
                "volume": s.get("volume", 0) or 0,
                "max_price": s.get("maxPrice", 0) or 0,
                "min_price": s.get("minPrice", 0) or 0,
                "opening_price": s.get("openingPrice", 0) or 0,
                "previous_closing": s.get("previousClosing", 0) or 0,
                "no_of_transactions": s.get("noOfTransactions", 0) or 0,
                "amount": s.get("amount", 0) or 0,
            })
        return formatted_list
    except Exception as e:
        logger.error(f"Error getting stock list: {e}")
        return []
