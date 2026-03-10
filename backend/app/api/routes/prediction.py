"""Prediction API routes."""

from fastapi import APIRouter

from app.services.prediction_service import predict_trend

router = APIRouter(tags=["Prediction"])


@router.get("/stocks/{symbol}/prediction")
async def get_prediction(symbol: str):
    """Get stock price prediction and trend analysis."""
    return await predict_trend(symbol)
