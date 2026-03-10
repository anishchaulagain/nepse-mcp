"""Adapters for external NEPSE data APIs."""

import httpx
import pandas as pd
from datetime import datetime
from typing import Optional, Dict, Any
from app.utils.logger import get_logger

logger = get_logger(__name__)

async def fetch_chukul_data(symbol: str, days: int = 365) -> Optional[pd.DataFrame]:
    """
    Fetch OHLCV data from Chukul.com.
    Endpoint: https://chukul.com/api/data/adjhistorydata/data/?symbol={symbol}&from={from_ts}&to={to_ts}
    """
    to_ts = int(datetime.now().timestamp())
    from_ts = to_ts - (days * 24 * 60 * 60)
    
    url = f"https://chukul.com/api/data/adjhistorydata/data/?symbol={symbol.upper()}&from={from_ts}&to={to_ts}"
    
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
    Endpoint: https://nepalipaisa.com/api/GetStockDataForChart?stockSymbol={symbol}&dataType=1D&_=timestamp
    """
    symbol = symbol.upper()
    ts = int(datetime.now().timestamp() * 1000)
    url = f"https://nepalipaisa.com/api/GetStockDataForChart?stockSymbol={symbol}&dataType=1D&_={ts}"
    
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
