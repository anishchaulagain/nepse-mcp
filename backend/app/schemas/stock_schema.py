"""Pydantic schemas for stock data."""

from pydantic import BaseModel
from typing import Optional


class CandleData(BaseModel):
    timestamp: list[int]
    open: list[float]
    high: list[float]
    low: list[float]
    close: list[float]
    volume: list[float]
    amount: list[float] = []


class StockInfo(BaseModel):
    symbol: str
    name: str
    sector: str
    last_price: float
    change: float
    change_percent: float
    volume: int


class StockListResponse(BaseModel):
    stocks: list[StockInfo]


class CandleResponse(BaseModel):
    symbol: str
    timeframe: str
    candles: list[dict]
    total: int
