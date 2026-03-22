"""Adapters for external NEPSE data APIs."""

import httpx
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def fetch_chukul_data(symbol: str, days: int = 365) -> Optional[pd.DataFrame]:
    """
    Fetch OHLCV data from Chukul.com.
    """
    settings = get_settings()
    to_ts = int(datetime.now().timestamp())
    from_ts = to_ts - (days * 24 * 60 * 60)
    
    url = f"{settings.CHUKUL_API_URL}?symbol={symbol.upper()}&from={from_ts}&to={to_ts}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data or "t" not in data:
                logger.warning(f"No valid data returned from Chukul for {symbol}")
                return None
            
            # Chukul returns: {"t": [...], "o": [...], "h": [...], "l": [...], "c": [...], "vol": [...]}
            df = pd.DataFrame({
                "timestamp": pd.to_datetime(data["t"], unit="s"),
                "open": data["o"],
                "high": data["h"],
                "low": data["l"],
                "close": data["c"],
                "volume": data["vol"],
            })
            
            return df
            
    except Exception as e:
        logger.error(f"Error fetching Chukul data for {symbol}: {e}")
        return None

async def fetch_nepalipaisa_data(symbol: str) -> Optional[Dict[str, Any]]:
    """
    Fetch recent chart data from Nepali Paisa.
    """
    settings = get_settings()
    symbol = symbol.upper()
    ts = int(datetime.now().timestamp() * 1000)
    url = f"{settings.NEPALI_PAISA_API_URL}?stockSymbol={symbol}&dataType=1D&_={ts}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("statusCode") == 200 and data.get("result"):
                return data["result"]
            
            return None
            
    except Exception as e:
        logger.error(f"Error fetching Nepali Paisa data for {symbol}: {e}")
        return None

_chukul_symbols_cache = None
_chukul_symbols_cache_time = 0

async def fetch_chukul_symbols() -> list[Dict[str, Any]]:
    """
    Fetch the list of available NEPSE symbols from Chukul.com.
    Uses an in-memory 1-hour cache to avoid duplicate calls.
    """
    global _chukul_symbols_cache, _chukul_symbols_cache_time
    
    now = datetime.now().timestamp()
    if _chukul_symbols_cache is not None and (now - _chukul_symbols_cache_time < 3600):
        # Return cached list if less than 1 hour old
        return _chukul_symbols_cache

    settings = get_settings()
    url = settings.CHUKUL_SYMBOL_API_URL
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                _chukul_symbols_cache = data
                _chukul_symbols_cache_time = now
                return data
            return []
            
    except Exception as e:
        logger.error(f"Error fetching Chukul symbols: {e}")
        # Return stale cache if available, otherwise empty
        return _chukul_symbols_cache if _chukul_symbols_cache is not None else []

_nepalipaisa_live_stocks_cache = None
_nepalipaisa_live_stocks_cache_time = 0

async def fetch_nepalipaisa_live_stocks() -> list[Dict[str, Any]]:
    """
    Fetch live stock data from Nepali Paisa.
    Uses an in-memory 1-minute cache.
    """
    global _nepalipaisa_live_stocks_cache, _nepalipaisa_live_stocks_cache_time
    
    now = datetime.now().timestamp()
    if _nepalipaisa_live_stocks_cache is not None and (now - _nepalipaisa_live_stocks_cache_time < 60):
        return _nepalipaisa_live_stocks_cache

    settings = get_settings()
    ts = int(now * 1000)
    url = f"{settings.NEPALI_PAISA_LIVE_STOCKS_URL}?stockSymbol=&_={ts}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data.get("statusCode") == 200 and data.get("result") and "stocks" in data["result"]:
                stocks = data["result"]["stocks"]
                _nepalipaisa_live_stocks_cache = stocks
                _nepalipaisa_live_stocks_cache_time = now
                return stocks
            return []
            
    except Exception as e:
        logger.error(f"Error fetching Nepali Paisa live stocks: {e}")
        return _nepalipaisa_live_stocks_cache if _nepalipaisa_live_stocks_cache is not None else []
