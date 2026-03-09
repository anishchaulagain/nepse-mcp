"use client";

import { useEffect, useRef } from "react";
import { createChart, ColorType, type IChartApi } from "lightweight-charts";
import type { Candle } from "@/types";

interface CandleChartProps {
  candles: Candle[];
  symbol: string;
  sma20?: number[];
  sma50?: number[];
  height?: number;
}

export default function CandleChart({
  candles,
  symbol,
  sma20,
  sma50,
  height = 500,
}: CandleChartProps) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current || candles.length === 0) return;

    // Cleanup previous chart
    if (chartRef.current) {
      chartRef.current.remove();
      chartRef.current = null;
    }

    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: "transparent" },
        textColor: "#8888a0",
        fontFamily: "Inter, system-ui, sans-serif",
      },
      grid: {
        vertLines: { color: "rgba(42, 42, 62, 0.5)" },
        horzLines: { color: "rgba(42, 42, 62, 0.5)" },
      },
      width: chartContainerRef.current.clientWidth,
      height: height,
      crosshair: {
        mode: 0,
        vertLine: {
          color: "rgba(99, 102, 241, 0.3)",
          labelBackgroundColor: "#6366f1",
        },
        horzLine: {
          color: "rgba(99, 102, 241, 0.3)",
          labelBackgroundColor: "#6366f1",
        },
      },
      timeScale: {
        borderColor: "#2a2a3e",
        timeVisible: false,
      },
      rightPriceScale: {
        borderColor: "#2a2a3e",
      },
    });

    chartRef.current = chart;

    // Candlestick series
    const candleSeries = chart.addCandlestickSeries({
      upColor: "#10b981",
      downColor: "#ef4444",
      borderUpColor: "#10b981",
      borderDownColor: "#ef4444",
      wickUpColor: "#10b981",
      wickDownColor: "#ef4444",
    });

    const candleData = candles.map((c) => ({
      time: c.time as string,
      open: c.open,
      high: c.high,
      low: c.low,
      close: c.close,
    }));

    candleSeries.setData(candleData as any);

    // Volume series
    const volumeSeries = chart.addHistogramSeries({
      color: "#6366f1",
      priceFormat: { type: "volume" },
      priceScaleId: "volume",
    });

    chart.priceScale("volume").applyOptions({
      scaleMargins: { top: 0.8, bottom: 0 },
    });

    const volumeData = candles.map((c) => ({
      time: c.time as string,
      value: c.volume,
      color: c.close >= c.open ? "rgba(16, 185, 129, 0.3)" : "rgba(239, 68, 68, 0.3)",
    }));

    volumeSeries.setData(volumeData as any);

    // SMA overlays
    if (sma20 && sma20.length === candles.length) {
      const sma20Series = chart.addLineSeries({
        color: "#f59e0b",
        lineWidth: 1,
        title: "SMA20",
      });
      sma20Series.setData(
        candles.map((c, i) => ({ time: c.time as string, value: sma20[i] })) as any
      );
    }

    if (sma50 && sma50.length === candles.length) {
      const sma50Series = chart.addLineSeries({
        color: "#06b6d4",
        lineWidth: 1,
        title: "SMA50",
      });
      sma50Series.setData(
        candles.map((c, i) => ({ time: c.time as string, value: sma50[i] })) as any
      );
    }

    chart.timeScale().fitContent();

    // Resize handler
    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ width: chartContainerRef.current.clientWidth });
      }
    };

    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      chart.remove();
      chartRef.current = null;
    };
  }, [candles, sma20, sma50, height]);

  return (
    <div className="glass-card p-4">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-[var(--color-text-primary)]">
          {symbol} — Price Chart
        </h3>
        <div className="flex items-center gap-3 text-xs text-[var(--color-text-secondary)]">
          <span className="flex items-center gap-1">
            <span className="w-3 h-0.5 bg-amber-400 rounded" /> SMA20
          </span>
          <span className="flex items-center gap-1">
            <span className="w-3 h-0.5 bg-cyan-400 rounded" /> SMA50
          </span>
        </div>
      </div>
      <div ref={chartContainerRef} />
    </div>
  );
}
