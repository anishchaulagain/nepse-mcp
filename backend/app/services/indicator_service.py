"""Indicator service — orchestrates technical indicator calculations."""

from app.services.nepse_service import get_stock_candles
from app.core.indicators.sma import get_sma_values
from app.core.indicators.rsi import get_rsi_value
from app.core.indicators.macd import get_macd_values
from app.core.indicators.bollinger import get_bollinger_values
from app.core.prediction_engine import detect_volume_spike
from app.schemas.indicator_schema import IndicatorResponse, SMAValues, MACDValues, BollingerValues
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def calculate_indicators(symbol: str) -> IndicatorResponse:
    """Calculate all technical indicators for a given stock symbol."""
    logger.info(f"Calculating indicators for {symbol}")
    df = await get_stock_candles(symbol)

    sma = get_sma_values(df)
    rsi = get_rsi_value(df)
    macd = get_macd_values(df)
    bollinger = get_bollinger_values(df)
    volume = detect_volume_spike(df)

    return IndicatorResponse(
        symbol=symbol.upper(),
        rsi=rsi["value"],
        sma=SMAValues(
            sma20=sma["sma20"],
            sma50=sma["sma50"],
            sma200=sma["sma200"],
        ),
        macd=MACDValues(
            macd_line=macd["macd_line"],
            signal_line=macd["signal_line"],
            histogram=macd["histogram"],
            trend=macd["trend"],
        ),
        bollinger=BollingerValues(
            upper=bollinger["upper"],
            middle=bollinger["middle"],
            lower=bollinger["lower"],
            bandwidth=bollinger["bandwidth"],
        ),
        volume_spike=volume["spike"],
        volume_avg=volume["avg_volume"],
        current_price=round(float(df["close"].iloc[-1]), 2),
    )


async def get_indicator_series(symbol: str) -> dict:
    """Get full indicator time series for charting."""
    df = await get_stock_candles(symbol)
    sma = get_sma_values(df)

    return {
        "timestamps": df["timestamp"].dt.strftime("%Y-%m-%d").tolist(),
        "sma20": sma["sma20_series"].round(2).tolist(),
        "sma50": sma["sma50_series"].round(2).tolist(),
        "sma200": sma["sma200_series"].round(2).tolist(),
    }
