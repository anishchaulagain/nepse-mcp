"""Backtesting service for NEPSE AI strategies."""

import pandas as pd
import numpy as np
from typing import List, Dict
from app.services.nepse_service import get_stock_candles
from app.core.prediction_engine import run_prediction
from app.utils.logger import get_logger

logger = get_logger(__name__)


async def run_backtest(symbol: str, initial_capital: float = 100000.0, days: int = 180) -> dict:
    """Run a simple backtest of the rule-based prediction engine.

    Strategy:
    - BUY when trend is "bullish" or "oversold"
    - SELL when trend is "bearish" or "overbought"
    - Hold otherwise
    """
    logger.info(f"Running backtest for {symbol} over {days} days")
    df = await get_stock_candles(symbol, days=days + 50)  # Extra days for indicator smoothing

    capital = initial_capital
    position = 0
    trades: List[Dict] = []  # List of trade dictionaries
    equity_curve: List[Dict] = []  # List of dictionaries with 'time' and 'value'

    # Iterate through days (sliding window for prediction)
    for i in range(50, len(df)):
        current_df = df.iloc[: i + 1]
        prediction = run_prediction(current_df)
        price = float(df["close"].iloc[i])
        date = df["timestamp"].iloc[i].strftime("%Y-%m-%d")

        trend = prediction["trend"]

        # Logic
        if trend in ["bullish", "oversold"] and position == 0:
            # Buy
            shares = capital // price
            if shares > 0:
                cost = shares * price
                capital -= cost
                position = shares
                trades.append({
                    "date": date,
                    "type": "buy",
                    "price": price,
                    "shares": shares,
                    "reason": trend
                })

        elif trend in ["bearish", "overbought"] and position > 0:
            # Sell
            revenue = position * price
            capital += revenue
            trades.append({
                "date": date,
                "type": "sell",
                "price": price,
                "shares": position,
                "reason": trend
            })
            position = 0

        # Current total value
        total_value = capital + (position * price)
        equity_curve.append({"time": date, "value": round(total_value, 2)})

    # Final Sell if still holding
    if position > 0:
        price = float(df["close"].iloc[-1])
        capital += position * price
        trades.append({
            "date": df["timestamp"].iloc[-1].strftime("%Y-%m-%d"),
            "type": "sell",
            "price": price,
            "shares": position,
            "reason": "end_of_backtest"
        })
        position = 0

    total_return = ((capital - initial_capital) / initial_capital) * 100
    buy_and_hold_return = ((float(df["close"].iloc[-1]) - float(df["close"].iloc[50])) / float(df["close"].iloc[50])) * 100

    # Calculate win rate
    win_rate = 0
    if len(trades) >= 2:
        profits = []
        for i in range(0, len(trades) - 1, 2):
            if i + 1 < len(trades):
                buy = trades[i]
                sell = trades[i+1]
                profit = (sell["price"] - buy["price"]) * buy["shares"]
                profits.append(profit > 0)
        if profits:
            win_rate = (sum(profits) / len(profits)) * 100

    return {
        "symbol": symbol.upper(),
        "initial_capital": initial_capital,
        "final_capital": round(capital, 2),
        "total_return_pct": round(total_return, 2),
        "buy_and_hold_return_pct": round(buy_and_hold_return, 2),
        "trades_count": len(trades),
        "win_rate_pct": round(win_rate, 2),
        "equity_curve": equity_curve,
        "trades": trades
    }
