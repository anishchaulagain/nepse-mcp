"""Pydantic schemas for technical indicators."""

from pydantic import BaseModel
from typing import Optional


class SMAValues(BaseModel):
    sma20: Optional[float] = None
    sma50: Optional[float] = None
    sma200: Optional[float] = None


class MACDValues(BaseModel):
    macd_line: Optional[float] = None
    signal_line: Optional[float] = None
    histogram: Optional[float] = None
    trend: str = "neutral"


class BollingerValues(BaseModel):
    upper: Optional[float] = None
    middle: Optional[float] = None
    lower: Optional[float] = None
    bandwidth: Optional[float] = None


class IndicatorResponse(BaseModel):
    symbol: str
    rsi: Optional[float] = None
    sma: SMAValues
    macd: MACDValues
    bollinger: BollingerValues
    volume_spike: bool = False
    volume_avg: Optional[float] = None
    current_price: Optional[float] = None
