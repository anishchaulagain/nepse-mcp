"use client";

import { useState, useEffect } from "react";
import { getBacktest } from "@/lib/api";
import type { BacktestResponse, BacktestTrade } from "@/types";
import {
  TrendingUp,
  TrendingDown,
  History,
  Play,
  ArrowUpRight,
  ArrowDownRight,
  Loader2,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { formatPrice, getChangeColor } from "@/lib/utils";

interface BacktestPanelProps {
  symbol: string;
}

export default function BacktestPanel({ symbol }: BacktestPanelProps) {
  const [data, setData] = useState<BacktestResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState(180);

  const runTest = async () => {
    setLoading(true);
    try {
      const res = await getBacktest(symbol, days);
      setData(res);
    } catch (error) {
      console.error("Backtest failed:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runTest();
  }, [symbol]);

  return (
    <div className="glass-card p-5 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <History className="w-5 h-5 text-indigo-400" />
          <h3 className="text-sm font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider">
            AI Strategy Backtest
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="bg-[var(--color-surface-elevated)] border border-[var(--color-border)] text-xs rounded-lg px-2 py-1 focus:outline-none"
          >
            <option value={90}>3 Months</option>
            <option value={180}>6 Months</option>
            <option value={365}>1 Year</option>
          </select>
          <button
            onClick={runTest}
            disabled={loading}
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-indigo-500 hover:bg-indigo-600 disabled:opacity-50 text-xs font-bold transition-all"
          >
            {loading ? <Loader2 className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3" />}
            Run Test
          </button>
        </div>
      </div>

      {data ? (
        <div className="space-y-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white/5 p-3 rounded-xl border border-white/10">
              <p className="text-[10px] text-[var(--color-text-secondary)] uppercase">Total Return</p>
              <p className={`text-lg font-bold ${getChangeColor(data.total_return_pct)}`}>
                {data.total_return_pct > 0 ? "+" : ""}
                {data.total_return_pct}%
              </p>
            </div>
            <div className="bg-white/5 p-3 rounded-xl border border-white/10">
              <p className="text-[10px] text-[var(--color-text-secondary)] uppercase">Win Rate</p>
              <p className="text-lg font-bold text-indigo-400">{data.win_rate_pct}%</p>
            </div>
            <div className="bg-white/5 p-3 rounded-xl border border-white/10">
              <p className="text-[10px] text-[var(--color-text-secondary)] uppercase">Trades</p>
              <p className="text-lg font-bold text-[var(--color-text-primary)]">{data.trades_count}</p>
            </div>
            <div className="bg-white/5 p-3 rounded-xl border border-white/10">
              <p className="text-[10px] text-[var(--color-text-secondary)] uppercase">Final Value</p>
              <p className="text-lg font-bold text-[var(--color-text-primary)]">
                {Math.round(data.final_capital / 1000)}k
              </p>
            </div>
          </div>

          {/* Equity Chart */}
          <div className="h-48 w-full border-t border-[var(--color-border)] pt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data.equity_curve}>
                <defs>
                  <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#2a2a3e" vertical={false} />
                <XAxis dataKey="time" hide />
                <YAxis hide domain={["auto", "auto"]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#12121a",
                    borderColor: "#2a2a3e",
                    borderRadius: "8px",
                  }}
                  itemStyle={{ color: "#e4e4ef" }}
                  labelStyle={{ display: "none" }}
                />
                <Area
                  type="monotone"
                  dataKey="value"
                  stroke="#6366f1"
                  fillOpacity={1}
                  fill="url(#colorValue)"
                />
              </AreaChart>
            </ResponsiveContainer>
            <div className="flex justify-between text-[10px] text-[var(--color-text-secondary)] mt-1">
              <span>Start ({data.equity_curve[0]?.time})</span>
              <span>Equity Curve</span>
              <span>End ({data.equity_curve[data.equity_curve.length - 1]?.time})</span>
            </div>
          </div>

          {/* Recent Trades List */}
          <div className="space-y-2">
            <h4 className="text-[10px] font-bold text-[var(--color-text-secondary)] uppercase tracking-wider">
              Recent Trade History
            </h4>
            <div className="max-h-40 overflow-y-auto space-y-1.5 pr-2">
              {data.trades
                .slice()
                .reverse()
                .map((trade: BacktestTrade, i: number) => (
                  <div
                    key={i}
                    className="flex items-center justify-between p-2 rounded-lg bg-white/5 border border-white/5 text-xs"
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`p-1.5 rounded-lg ${
                          trade.type === "buy" ? "bg-emerald-500/10" : "bg-red-500/10"
                        }`}
                      >
                        {trade.type === "buy" ? (
                          <ArrowUpRight className="w-3 h-3 text-emerald-400" />
                        ) : (
                          <ArrowDownRight className="w-3 h-3 text-red-400" />
                        )}
                      </div>
                      <div>
                        <p className="font-semibold capitalize">
                          {trade.type} {symbol}
                        </p>
                        <p className="text-[10px] text-[var(--color-text-secondary)]">
                          {trade.date} • {trade.reason}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-mono">{formatPrice(trade.price)}</p>
                      <p className="text-[10px] text-[var(--color-text-secondary)]">
                        {trade.shares} shares
                      </p>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      ) : (
        <div className="h-64 flex flex-col items-center justify-center text-[var(--color-text-secondary)] animate-pulse">
          <History className="w-8 h-8 mb-2 opacity-50" />
          <p className="text-sm">Running backtest simulation...</p>
        </div>
      )}
    </div>
  );
}
