"""Prediction API routes."""

from fastapi import APIRouter

from app.services.prediction_service import predict_trend

router = APIRouter(tags=["Prediction"])


@router.get("/stocks/{symbol}/prediction")
async def get_prediction(symbol: str):
    """Get AI prediction for a stock."""
    result = predict_trend(symbol)
    return result.model_dump()
