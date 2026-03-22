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
async def get_breakout_analysis(symbol: str):
    """Detect breakout signals for a stock."""
    result = await detect_breakout(symbol)
    return result.model_dump()


@router.get("/stocks/{symbol}/analysis")
async def full_analysis(symbol: str):
    """Get full AI analysis for a stock: indicators + prediction + breakout + AI explanation."""
    indicators = await calculate_indicators(symbol)
    prediction = await predict_trend(symbol)
    breakout = await detect_breakout(symbol)

    df = await get_stock_candles(symbol)
    current_price = round(float(df["close"].iloc[-1]), 2)

    # Generate AI explanation using Groq
    ai_explanation = ""
    ai_recommendation = "HOLD"
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

Provide a decisive recommendation for a retail investor. You must strictly follow this exact format:
Recommendation: [BUY or SELL or HOLD]
Analysis: [A concise 2-3 sentence analysis in simple language explaining the recommendation, trend direction, and key risks.]"""

            chat = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300,
            )
            response_content = chat.choices[0].message.content or ""
            
            # Parse the response
            # Format expected:
            # Recommendation: BUY
            # Analysis: ...
            parsed_recommendation = None
            parsed_analysis = None
            
            for line in response_content.split('\n'):
                line = line.strip()
                if line.upper().startswith("RECOMMENDATION:"):
                    raw_rec = line.split(":", 1)[1].strip().upper()
                    # Clean up punctuation if any
                    for word in ["BUY", "SELL", "HOLD"]:
                        if word in raw_rec:
                            parsed_recommendation = word
                            break
                    if not parsed_recommendation:
                        parsed_recommendation = "HOLD"
                elif line.upper().startswith("ANALYSIS:"):
                    parsed_analysis = line.split(":", 1)[1].strip()
            
            # In case LLM doesn't strict format, we do our best
            if not parsed_analysis:
                # If we couldn't parse Analysis:, just take the text after "Recommendation:"
                if "RECOMMENDATION:" in response_content.upper():
                    parts = response_content.upper().split("RECOMMENDATION:", 1)
                    if len(parts) > 1:
                        # Extract the next line usually
                        try:
                            # It's a rough fallback
                            after_rec = parts[1].split("\n", 1)
                            if len(after_rec) > 1:
                                parsed_analysis = after_rec[1].strip()
                        except:
                            parsed_analysis = response_content
                else:
                    parsed_analysis = response_content

            ai_recommendation = parsed_recommendation or "HOLD"
            ai_explanation = parsed_analysis or response_content
            
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
        "ai_recommendation": ai_recommendation,
        "timestamp": datetime.now().isoformat(),
    }
