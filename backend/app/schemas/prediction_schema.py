"""Pydantic schemas for predictions and breakout detection."""

from pydantic import BaseModel
from typing import Optional


class PredictionResponse(BaseModel):
    symbol: str
    trend: str  # bullish, bearish, sideways, overbought, oversold
    confidence: float
    signals: list[str]
    summary: str = ""


class BreakoutResponse(BaseModel):
    symbol: str
    breakout: bool
    type: str  # bullish, bearish, none
    confidence: float
    reasons: list[str] = []


class FullAnalysisResponse(BaseModel):
    symbol: str
    current_price: Optional[float] = None
    indicators: dict
    prediction: dict
    breakout: dict
    ai_explanation: str = ""
    timestamp: str = ""
