/* API client for NEPSE AI backend */

import type {
  StockListResponse,
  CandleResponse,
  IndicatorResponse,
  PredictionResponse,
  BreakoutResponse,
  FullAnalysis,
  BacktestResponse,
} from "@/types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function fetchAPI<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    cache: "no-store",
  });

  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

export async function getStocks(): Promise<StockListResponse> {
  return fetchAPI<StockListResponse>("/stocks");
}

export async function getCandles(symbol: string, days: number = 365): Promise<CandleResponse> {
  return fetchAPI<CandleResponse>(`/stocks/${symbol}/candles?days=${days}`);
}

export async function getIndicators(symbol: string): Promise<IndicatorResponse> {
  return fetchAPI<IndicatorResponse>(`/stocks/${symbol}/indicators`);
}

export async function getPrediction(symbol: string): Promise<PredictionResponse> {
  return fetchAPI<PredictionResponse>(`/stocks/${symbol}/prediction`);
}

export async function getBreakout(symbol: string): Promise<BreakoutResponse> {
  return fetchAPI<BreakoutResponse>(`/stocks/${symbol}/breakout`);
}

export async function getFullAnalysis(symbol: string): Promise<FullAnalysis> {
  return fetchAPI<FullAnalysis>(`/stocks/${symbol}/analysis`);
}

export async function getBacktest(
  symbol: string,
  days: number = 180,
  initialCapital: number = 100000
): Promise<BacktestResponse> {
  return fetchAPI<BacktestResponse>(
    `/stocks/${symbol}/backtest?days=${days}&initial_capital=${initialCapital}`
  );
}
