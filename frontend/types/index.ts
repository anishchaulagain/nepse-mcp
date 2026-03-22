/* TypeScript types for NEPSE AI Platform */

export interface StockInfo {
  symbol: string;
  name: string;
  sector: string;
  last_price: number;
  change: number;
  change_percent: number;
  volume: number;
  max_price?: number;
  min_price?: number;
  opening_price?: number;
  previous_closing?: number;
  difference_rs?: number;
  no_of_transactions?: number;
  amount?: number;
}

export interface Candle {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface CandleResponse {
  symbol: string;
  timeframe: string;
  candles: Candle[];
  total: number;
}

export interface SMAValues {
  sma20: number | null;
  sma50: number | null;
  sma200: number | null;
}

export interface MACDValues {
  macd_line: number | null;
  signal_line: number | null;
  histogram: number | null;
  trend: string;
}

export interface BollingerValues {
  upper: number | null;
  middle: number | null;
  lower: number | null;
  bandwidth: number | null;
}

export interface IndicatorResponse {
  symbol: string;
  rsi: number | null;
  sma: SMAValues;
  macd: MACDValues;
  bollinger: BollingerValues;
  volume_spike: boolean;
  volume_avg: number | null;
  current_price: number | null;
}

export interface PredictionResponse {
  symbol: string;
  trend: string;
  confidence: number;
  signals: string[];
  summary: string;
}

export interface BreakoutResponse {
  symbol: string;
  breakout: boolean;
  type: string;
  confidence: number;
  reasons: string[];
}

export interface FullAnalysis {
  symbol: string;
  current_price: number;
  indicators: IndicatorResponse;
  prediction: PredictionResponse;
  breakout: BreakoutResponse;
  ai_explanation: string;
  ai_recommendation: string;
  timestamp: string;
}

export interface StockListResponse {
  stocks: StockInfo[];
  total: number;
}

export interface BacktestTrade {
  date: string;
  type: "buy" | "sell";
  price: number;
  shares: number;
  reason: string;
}

export interface EquityPoint {
  time: string;
  value: number;
}

export interface BacktestResponse {
  symbol: string;
  initial_capital: number;
  final_capital: number;
  total_return_pct: number;
  buy_and_hold_return_pct: number;
  trades_count: number;
  win_rate_pct: number;
  equity_curve: EquityPoint[];
  trades: BacktestTrade[];
}
