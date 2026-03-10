"""NEPSE data service — fetches/generates OHLCV data for stocks."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Top NEPSE stocks with realistic sectors and metadata
NEPSE_STOCKS = {
    "NABIL": {"name": "Nabil Bank Limited", "sector": "Commercial Banks", "base_price": 350},
    "NICA": {"name": "NIC Asia Bank Limited", "sector": "Commercial Banks", "base_price": 280},
    "GBIME": {"name": "Global IME Bank Limited", "sector": "Commercial Banks", "base_price": 240},
    "SBL": {"name": "Siddhartha Bank Limited", "sector": "Commercial Banks", "base_price": 220},
    "HBL": {"name": "Himalayan Bank Limited", "sector": "Commercial Banks", "base_price": 310},
    "ADBL": {"name": "Agricultural Dev Bank", "sector": "Commercial Banks", "base_price": 290},
    "SCB": {"name": "Standard Chartered Bank", "sector": "Commercial Banks", "base_price": 450},
    "NLIC": {"name": "Nepal Life Insurance", "sector": "Life Insurance", "base_price": 520},
    "ALICL": {"name": "Asian Life Insurance", "sector": "Life Insurance", "base_price": 460},
    "PLIC": {"name": "Premier Life Insurance", "sector": "Life Insurance", "base_price": 410},
    "CHCL": {"name": "Chilime Hydropower", "sector": "Hydropower", "base_price": 380},
    "NHPC": {"name": "Nepal Hydro Developers", "sector": "Hydropower", "base_price": 340},
    "BPCL": {"name": "Butwal Power Company", "sector": "Hydropower", "base_price": 300},
    "UPPER": {"name": "Upper Tamakoshi", "sector": "Hydropower", "base_price": 270},
    "NTC": {"name": "Nepal Telecom", "sector": "Telecom", "base_price": 600},
    "SHIVM": {"name": "Shivam Cements", "sector": "Manufacturing", "base_price": 340},
    "UNL": {"name": "Unilever Nepal", "sector": "Manufacturing", "base_price": 8500},
    "NRIC": {"name": "Nepal Reinsurance", "sector": "Insurance", "base_price": 480},
    "SHL": {"name": "Soaltee Hotel Limited", "sector": "Hotels", "base_price": 260},
    "NMB": {"name": "NMB Bank Limited", "sector": "Commercial Banks", "base_price": 265},
}


def generate_mock_ohlcv(symbol: str, days: int = 365) -> pd.DataFrame:
    """Generate realistic mock OHLCV data for a given stock."""
    stock = NEPSE_STOCKS.get(symbol.upper())
    if not stock:
        stock = {"base_price": 300, "name": symbol, "sector": "Unknown"}

    np.random.seed(hash(symbol) % 2**32)

    base = stock["base_price"]
    dates = pd.date_range(end=datetime.now(), periods=days, freq="B")  # business days

    # Generate realistic price movement using geometric Brownian motion
    drift = 0.0002
    volatility = 0.018
    dt = 1.0

    returns = np.random.normal(drift, volatility, days)
    prices = base * np.exp(np.cumsum(returns))

    # Add some trend patterns
    trend = np.sin(np.linspace(0, 4 * np.pi, days)) * base * 0.08
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
    """Get list of available stocks with current info."""
    stocks = []
    for symbol, info in NEPSE_STOCKS.items():
        # Using real data if possible for the list
        try:
            df = await get_stock_candles(symbol, days=5)
            last_close = float(df["close"].iloc[-1])
            prev_close = float(df["close"].iloc[-2]) if len(df) >= 2 else last_close
            change = last_close - prev_close
            change_pct = (change / prev_close * 100) if prev_close != 0 else 0
            volume = int(df["volume"].iloc[-1])
        except Exception as e:
            logger.error(f"Error getting stock info for {symbol}: {e}")
            last_close = change = change_pct = volume = 0

        stocks.append({
            "symbol": symbol,
            "name": info["name"],
            "sector": info["sector"],
            "last_price": round(last_close, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "volume": volume,
        })

    return stocks
