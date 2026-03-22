import { getCandles, getIndicators, getPrediction, getBreakout, getFullAnalysis } from "@/lib/api";
import CandleChart from "@/components/charts/CandleChart";
import IndicatorPanel from "@/components/indicators/IndicatorPanel";
import PredictionCard from "@/components/predictions/PredictionCard";
import BacktestPanel from "@/components/predictions/BacktestPanel";
import { ArrowLeft, Activity } from "lucide-react";
import Link from "next/link";

export const dynamic = "force-dynamic";

interface StockPageProps {
  params: Promise<{ symbol: string }>;
}

export default async function StockDetailPage({ params }: StockPageProps) {
  const { symbol } = await params;
  const upperSymbol = symbol.toUpperCase();

  let candles: any = null;
  let indicators: any = null;
  let prediction: any = null;
  let breakout: any = null;
  let analysis: any = null;
  let indicatorSeries: any = null;
  let error = "";

  try {
    const [candleData, indicatorData, predictionData, breakoutData, analysisData] =
      await Promise.all([
        getCandles(upperSymbol),
        getIndicators(upperSymbol),
        getPrediction(upperSymbol),
        getBreakout(upperSymbol),
        getFullAnalysis(upperSymbol),
      ]);

    candles = candleData;
    indicators = indicatorData;
    prediction = predictionData;
    breakout = breakoutData;
    analysis = analysisData;

    // Fetch indicator series for SMA overlays
    try {
      const seriesRes = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}/stocks/${upperSymbol}/indicators/series`,
        { cache: "no-store" }
      );
      indicatorSeries = await seriesRes.json();
    } catch {}
  } catch (e: any) {
    error = e.message || "Failed to load data";
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6 animate-slide-up">
        <Link
          href="/"
          className="p-2 rounded-lg bg-[var(--color-surface-elevated)] border border-[var(--color-border)] hover:border-indigo-500/30 transition-all"
        >
          <ArrowLeft className="w-4 h-4 text-[var(--color-text-secondary)]" />
        </Link>
        <div>
          <h1 className="text-2xl font-extrabold gradient-text">{upperSymbol}</h1>
          {indicators?.current_price && (
            <p className="text-sm text-[var(--color-text-secondary)]">
              NPR {indicators.current_price.toFixed(2)}
            </p>
          )}
        </div>
        <div className="ml-auto flex items-center gap-2">
          <span className="pulse-dot bg-emerald-400" />
          <span className="text-xs text-[var(--color-text-secondary)]">Live Analysis</span>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div className="glass-card p-6 mb-6 border border-red-500/30 bg-red-500/5">
          <p className="text-red-400 text-sm">
            ⚠️ {error} — Make sure the backend is running on port 8000.
          </p>
        </div>
      )}

      {candles && (
        <div className="space-y-6">
          {/* Chart */}
          <div className="animate-slide-up" style={{ animationDelay: "100ms" }}>
            <CandleChart
              candles={candles.candles}
              symbol={upperSymbol}
              sma20={indicatorSeries?.sma20}
              sma50={indicatorSeries?.sma50}
            />
          </div>

          {/* Indicators + Prediction Grid */}
          <div
            className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-slide-up"
            style={{ animationDelay: "200ms" }}
          >
            {indicators && <IndicatorPanel indicators={indicators} />}
            {prediction && (
              <PredictionCard
                prediction={prediction}
                breakout={breakout}
                aiExplanation={analysis?.ai_explanation}
                aiRecommendation={analysis?.ai_recommendation}
              />
            )}
          </div>

          {/* Backtest Section */}
          <div className="animate-slide-up" style={{ animationDelay: "300ms" }}>
            <BacktestPanel symbol={upperSymbol} />
          </div>
        </div>
      )}

      {/* Empty state */}
      {!error && !candles && (
        <div className="glass-card p-12 text-center">
          <Activity className="w-12 h-12 text-[var(--color-text-secondary)] mx-auto mb-4 animate-pulse" />
          <h3 className="text-lg font-semibold mb-2">Loading analysis for {upperSymbol}...</h3>
          <p className="text-sm text-[var(--color-text-secondary)]">
            Fetching data and running AI predictions
          </p>
        </div>
      )}
    </div>
  );
}
