"""Rule-based AI prediction engine for NEPSE stocks."""

import pandas as pd
from app.core.indicators.sma import get_sma_values
from app.core.indicators.rsi import get_rsi_value
from app.core.indicators.macd import get_macd_values
from app.core.indicators.bollinger import get_bollinger_values


def detect_volume_spike(df: pd.DataFrame, threshold: float = 1.5) -> dict:
    """Detect volume spike by comparing latest volume to 20-day average."""
    vol = df["volume"]
    avg_volume = vol.rolling(window=20, min_periods=1).mean()
    latest_volume = float(vol.iloc[-1])
    avg_val = float(avg_volume.iloc[-1])

    spike = latest_volume > avg_val * threshold

    return {
        "spike": spike,
        "current_volume": latest_volume,
        "avg_volume": round(avg_val, 0),
        "ratio": round(latest_volume / avg_val, 2) if avg_val > 0 else 0,
    }


def run_prediction(df: pd.DataFrame) -> dict:
    """Run rule-based prediction engine.

    Returns: trend, confidence, signals list, summary.
    """
    if len(df) < 20:
        return {
            "trend": "insufficient_data",
            "confidence": 0.0,
            "signals": ["Not enough data for analysis (need at least 20 candles)"],
            "summary": "Insufficient data to make a prediction.",
        }

    price = float(df["close"].iloc[-1])
    sma = get_sma_values(df)
    rsi = get_rsi_value(df)
    macd = get_macd_values(df)
    bollinger = get_bollinger_values(df)
    volume = detect_volume_spike(df)

    signals = []
    bullish_score = 0
    bearish_score = 0
    total_checks = 0

    # --- SMA Analysis ---
    total_checks += 3

    if sma["sma50"] and price > sma["sma50"]:
        bullish_score += 1
        signals.append("Price above SMA50")
    elif sma["sma50"]:
        bearish_score += 1
        signals.append("Price below SMA50")

    if sma["sma20"] and sma["sma50"] and sma["sma20"] > sma["sma50"]:
        bullish_score += 1
        signals.append("SMA20 above SMA50 (golden cross zone)")
    elif sma["sma20"] and sma["sma50"]:
        bearish_score += 1
        signals.append("SMA20 below SMA50 (death cross zone)")

    if sma["sma200"] and price > sma["sma200"]:
        bullish_score += 1
        signals.append("Price above SMA200 (long-term bullish)")
    elif sma["sma200"]:
        bearish_score += 1
        signals.append("Price below SMA200 (long-term bearish)")

    # --- RSI Analysis ---
    total_checks += 1
    rsi_val = rsi["value"]
    if rsi_val is not None:
        if rsi_val >= 70:
            bearish_score += 1
            signals.append(f"RSI {rsi_val} — overbought")
        elif rsi_val <= 30:
            bullish_score += 1
            signals.append(f"RSI {rsi_val} — oversold (reversal possible)")
        elif rsi_val < 50:
            bearish_score += 0.5
            signals.append(f"RSI {rsi_val} — slightly bearish")
        else:
            bullish_score += 0.5
            signals.append(f"RSI {rsi_val} — neutral-to-bullish")

    # --- MACD Analysis ---
    total_checks += 1
    macd_trend = macd["trend"]
    if "bullish" in macd_trend:
        bullish_score += 1.5 if "crossover" in macd_trend else 1
        signals.append(f"MACD {macd_trend}")
    elif "bearish" in macd_trend:
        bearish_score += 1.5 if "crossover" in macd_trend else 1
        signals.append(f"MACD {macd_trend}")
    else:
        signals.append("MACD neutral")

    # --- Volume Analysis ---
    total_checks += 1
    if volume["spike"]:
        bullish_score += 0.5
        signals.append(f"Volume spike detected ({volume['ratio']}x avg)")

    # --- Bollinger Band Analysis ---
    total_checks += 1
    if bollinger["squeeze"]:
        signals.append("Bollinger squeeze — breakout imminent")
    if bollinger["band_position"] > 0.95:
        bearish_score += 0.5
        signals.append("Price near upper Bollinger Band")
    elif bollinger["band_position"] < 0.05:
        bullish_score += 0.5
        signals.append("Price near lower Bollinger Band (bounce possible)")

    # --- Determine Trend ---
    total_score = bullish_score + bearish_score
    confidence = 0.5

    if total_score > 0:
        confidence = max(bullish_score, bearish_score) / (total_score + 1)
        confidence = min(confidence, 0.95)

    # Determine final trend
    if rsi_val and rsi_val >= 70:
        trend = "overbought"
    elif rsi_val and rsi_val <= 30:
        trend = "oversold"
    elif bullish_score > bearish_score + 1:
        trend = "bullish"
    elif bearish_score > bullish_score + 1:
        trend = "bearish"
    elif bollinger["squeeze"] and volume["spike"]:
        trend = "breakout_possible"
    else:
        trend = "sideways"

    # Summary
    summaries = {
        "bullish": f"The stock shows bullish momentum with {len([s for s in signals if 'bullish' in s.lower() or 'above' in s.lower()])} positive signals.",
        "bearish": f"The stock is showing bearish pressure with multiple negative signals.",
        "sideways": "The stock is trading sideways with mixed signals. No clear trend.",
        "overbought": "The stock appears overbought. Consider taking profits or waiting for a pullback.",
        "oversold": "The stock appears oversold. A reversal or bounce may be incoming.",
        "breakout_possible": "Bollinger squeeze with volume spike suggests a breakout is imminent.",
        "insufficient_data": "Not enough data.",
    }

    return {
        "trend": trend,
        "confidence": round(confidence, 2),
        "signals": signals,
        "summary": summaries.get(trend, "Analysis complete."),
    }
