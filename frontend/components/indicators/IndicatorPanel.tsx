"use client";

import type { IndicatorResponse } from "@/types";
import { TrendingUp, TrendingDown, Activity, BarChart3 } from "lucide-react";

interface IndicatorPanelProps {
  indicators: IndicatorResponse;
}

export default function IndicatorPanel({ indicators }: IndicatorPanelProps) {
  const rsiColor =
    indicators.rsi && indicators.rsi >= 70
      ? "text-red-400"
      : indicators.rsi && indicators.rsi <= 30
        ? "text-emerald-400"
        : "text-amber-400";

  const macdIcon =
    indicators.macd.trend.includes("bullish") ? (
      <TrendingUp className="w-4 h-4 text-emerald-400" />
    ) : indicators.macd.trend.includes("bearish") ? (
      <TrendingDown className="w-4 h-4 text-red-400" />
    ) : (
      <Activity className="w-4 h-4 text-gray-400" />
    );

  return (
    <div className="glass-card p-5">
      <h3 className="text-sm font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider mb-4">
        Technical Indicators
      </h3>

      <div className="grid grid-cols-2 gap-4">
        {/* RSI */}
        <div className="space-y-1">
          <span className="text-xs text-[var(--color-text-secondary)]">RSI (14)</span>
          <div className={`text-2xl font-bold ${rsiColor}`}>
            {indicators.rsi?.toFixed(1) ?? "—"}
          </div>
          <div className="w-full h-1.5 bg-[var(--color-surface-elevated)] rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all ${
                indicators.rsi && indicators.rsi >= 70
                  ? "bg-red-500"
                  : indicators.rsi && indicators.rsi <= 30
                    ? "bg-emerald-500"
                    : "bg-amber-500"
              }`}
              style={{ width: `${indicators.rsi ?? 50}%` }}
            />
          </div>
          <div className="flex justify-between text-[10px] text-[var(--color-text-secondary)]">
            <span>Oversold</span>
            <span>Overbought</span>
          </div>
        </div>

        {/* MACD */}
        <div className="space-y-1">
          <span className="text-xs text-[var(--color-text-secondary)]">MACD</span>
          <div className="flex items-center gap-2">
            {macdIcon}
            <span className="text-lg font-semibold capitalize">
              {indicators.macd.trend.replace("_", " ")}
            </span>
          </div>
          <div className="text-xs text-[var(--color-text-secondary)] space-y-0.5">
            <div>Line: {indicators.macd.macd_line?.toFixed(4)}</div>
            <div>Signal: {indicators.macd.signal_line?.toFixed(4)}</div>
          </div>
        </div>

        {/* SMA */}
        <div className="space-y-1">
          <span className="text-xs text-[var(--color-text-secondary)]">Moving Averages</span>
          <div className="space-y-1.5 text-sm">
            <div className="flex justify-between">
              <span className="text-amber-400">SMA 20</span>
              <span className="font-mono">{indicators.sma.sma20?.toFixed(2) ?? "—"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-cyan-400">SMA 50</span>
              <span className="font-mono">{indicators.sma.sma50?.toFixed(2) ?? "—"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-violet-400">SMA 200</span>
              <span className="font-mono">{indicators.sma.sma200?.toFixed(2) ?? "—"}</span>
            </div>
          </div>
        </div>

        {/* Bollinger */}
        <div className="space-y-1">
          <span className="text-xs text-[var(--color-text-secondary)]">Bollinger Bands</span>
          <div className="space-y-1.5 text-sm">
            <div className="flex justify-between">
              <span className="text-red-400">Upper</span>
              <span className="font-mono">{indicators.bollinger.upper?.toFixed(2) ?? "—"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Middle</span>
              <span className="font-mono">{indicators.bollinger.middle?.toFixed(2) ?? "—"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-emerald-400">Lower</span>
              <span className="font-mono">{indicators.bollinger.lower?.toFixed(2) ?? "—"}</span>
            </div>
          </div>
        </div>

        {/* Volume */}
        <div className="col-span-2 flex items-center gap-4 pt-2 border-t border-[var(--color-border)]">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-indigo-400" />
            <span className="text-xs text-[var(--color-text-secondary)]">Volume</span>
          </div>
          <span className="text-sm font-mono">
            Avg: {indicators.volume_avg?.toLocaleString() ?? "—"}
          </span>
          {indicators.volume_spike && (
            <span className="trend-badge bg-violet-500/10 border-violet-500/30 text-violet-400">
              <span className="pulse-dot bg-violet-400" />
              Spike
            </span>
          )}
        </div>
      </div>
    </div>
  );
}
