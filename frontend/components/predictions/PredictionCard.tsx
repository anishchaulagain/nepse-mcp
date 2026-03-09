"use client";

import type { PredictionResponse, BreakoutResponse } from "@/types";
import {
  TrendingUp,
  TrendingDown,
  Minus,
  AlertTriangle,
  Zap,
  ArrowUpRight,
  ArrowDownRight,
  CheckCircle2,
} from "lucide-react";
import { getTrendColor, getTrendBg } from "@/lib/utils";

interface PredictionCardProps {
  prediction: PredictionResponse;
  breakout?: BreakoutResponse;
  aiExplanation?: string;
}

const trendIcons: Record<string, React.ReactNode> = {
  bullish: <TrendingUp className="w-6 h-6" />,
  bearish: <TrendingDown className="w-6 h-6" />,
  sideways: <Minus className="w-6 h-6" />,
  overbought: <AlertTriangle className="w-6 h-6" />,
  oversold: <ArrowDownRight className="w-6 h-6" />,
  breakout_possible: <Zap className="w-6 h-6" />,
};

export default function PredictionCard({
  prediction,
  breakout,
  aiExplanation,
}: PredictionCardProps) {
  const confidencePct = Math.round(prediction.confidence * 100);

  return (
    <div className="space-y-4">
      {/* Main Prediction */}
      <div className={`glass-card p-5 border ${getTrendBg(prediction.trend)}`}>
        <div className="flex items-start justify-between mb-4">
          <div>
            <span className="text-xs text-[var(--color-text-secondary)] uppercase tracking-wider">
              AI Prediction
            </span>
            <div className={`flex items-center gap-2 mt-1 ${getTrendColor(prediction.trend)}`}>
              {trendIcons[prediction.trend] || <Activity className="w-6 h-6" />}
              <span className="text-2xl font-bold capitalize">
                {prediction.trend.replace("_", " ")}
              </span>
            </div>
          </div>

          {/* Confidence ring */}
          <div className="relative w-16 h-16">
            <svg className="w-16 h-16 -rotate-90" viewBox="0 0 36 36">
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="rgba(42, 42, 62, 0.8)"
                strokeWidth="3"
              />
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke={confidencePct >= 60 ? "#10b981" : confidencePct >= 40 ? "#f59e0b" : "#ef4444"}
                strokeWidth="3"
                strokeDasharray={`${confidencePct}, 100`}
                strokeLinecap="round"
              />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-sm font-bold">{confidencePct}%</span>
            </div>
          </div>
        </div>

        {/* Signals */}
        <div className="space-y-1.5">
          {prediction.signals.map((signal, i) => (
            <div
              key={i}
              className="flex items-start gap-2 text-sm text-[var(--color-text-secondary)]"
            >
              <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 text-indigo-400 shrink-0" />
              <span>{signal}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Breakout Alert */}
      {breakout && breakout.breakout && (
        <div className="glass-card p-4 border border-violet-500/30 bg-violet-500/5">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-5 h-5 text-violet-400" />
            <span className="font-semibold text-violet-400 uppercase text-sm">
              Breakout Detected
            </span>
            <span className="trend-badge bg-violet-500/20 border-violet-500/40 text-violet-300 text-xs ml-auto">
              {breakout.type}
            </span>
          </div>
          <div className="space-y-1">
            {breakout.reasons.map((reason, i) => (
              <p key={i} className="text-sm text-[var(--color-text-secondary)]">
                • {reason}
              </p>
            ))}
          </div>
        </div>
      )}

      {/* AI Explanation */}
      {aiExplanation && (
        <div className="glass-card p-4">
          <span className="text-xs text-[var(--color-text-secondary)] uppercase tracking-wider">
            AI Analysis
          </span>
          <p className="mt-2 text-sm text-[var(--color-text-primary)] leading-relaxed">
            {aiExplanation}
          </p>
        </div>
      )}
    </div>
  );
}
