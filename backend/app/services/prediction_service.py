"""Prediction service — runs the prediction engine and optionally generates AI explanation."""

from app.services.nepse_service import get_stock_candles
from app.core.prediction_engine import run_prediction
from app.schemas.prediction_schema import PredictionResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


def predict_trend(symbol: str) -> PredictionResponse:
    """Run prediction engine for a given stock symbol."""
    logger.info(f"Running prediction for {symbol}")
    df = get_stock_candles(symbol)
    result = run_prediction(df)

    return PredictionResponse(
        symbol=symbol.upper(),
        trend=result["trend"],
        confidence=result["confidence"],
        signals=result["signals"],
        summary=result["summary"],
    )
