"""AI Analysis & Breakout API routes."""

from datetime import datetime
from fastapi import APIRouter

from app.services.indicator_service import calculate_indicators
from app.services.prediction_service import predict_trend
from app.services.breakout_service import detect_breakout
from app.services.nepse_service import get_stock_candles
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["AI Analysis"])


@router.get("/stocks/{symbol}/breakout")
async def get_breakout(symbol: str):
    """Detect breakout signals for a stock."""
    result = detect_breakout(symbol)
    return result.model_dump()


@router.get("/stocks/{symbol}/analysis")
async def full_analysis(symbol: str):
    """Get full AI analysis for a stock: indicators + prediction + breakout + AI explanation."""
    indicators = calculate_indicators(symbol)
    prediction = predict_trend(symbol)
    breakout = detect_breakout(symbol)

    df = get_stock_candles(symbol)
    current_price = round(float(df["close"].iloc[-1]), 2)

    # Generate AI explanation using Groq
    ai_explanation = ""
    settings = get_settings()

    if settings.GROQ_API_KEY:
        try:
            from groq import Groq

            client = Groq(api_key=settings.GROQ_API_KEY)

            prompt = f"""You are a NEPSE (Nepal Stock Exchange) financial analyst.
Analyze {symbol} stock based on these indicators:

Current Price: NPR {current_price}
RSI: {indicators.rsi}
SMA20: {indicators.sma.sma20}, SMA50: {indicators.sma.sma50}, SMA200: {indicators.sma.sma200}
MACD Trend: {indicators.macd.trend}
Bollinger Bandwidth: {indicators.bollinger.bandwidth}
Volume Spike: {indicators.volume_spike}

Prediction: {prediction.trend} (confidence: {prediction.confidence})
Breakout: {breakout.breakout} ({breakout.type})
Signals: {', '.join(prediction.signals)}

Provide a concise 3-4 sentence analysis in simple language. Focus on what a retail investor should know. Include the trend direction, key risk, and a suggestion."""

            chat = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            ai_explanation = chat.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq LLM error: {e}")
            ai_explanation = prediction.summary

    else:
        ai_explanation = prediction.summary

    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "indicators": indicators.model_dump(),
        "prediction": prediction.model_dump(),
        "breakout": breakout.model_dump(),
        "ai_explanation": ai_explanation,
        "timestamp": datetime.now().isoformat(),
    }
