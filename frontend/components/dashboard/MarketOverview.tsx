"use client";

import Link from "next/link";
import type { StockInfo } from "@/types";
import { TrendingUp, TrendingDown, BarChart3, ArrowRight } from "lucide-react";
import { getChangeColor, formatPrice, formatVolume } from "@/lib/utils";

interface MarketOverviewProps {
  stocks: StockInfo[];
}

export default function MarketOverview({ stocks }: MarketOverviewProps) {
  const gainers = [...stocks].sort((a, b) => b.change_percent - a.change_percent).slice(0, 5);
  const losers = [...stocks].sort((a, b) => a.change_percent - b.change_percent).slice(0, 5);
  const mostActive = [...stocks].sort((a, b) => b.volume - a.volume).slice(0, 5);

  return (
    <div className="space-y-6">
      {/* Market Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="glass-card p-5 glow-accent">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-emerald-400" />
            </div>
            <div>
              <p className="text-xs text-[var(--color-text-secondary)]">Top Gainers</p>
              <p className="text-lg font-bold text-emerald-400">
                {gainers[0]?.symbol ?? "—"}
              </p>
            </div>
          </div>
          <p className="text-sm text-emerald-400 font-semibold">
            +{gainers[0]?.change_percent?.toFixed(2) ?? 0}%
          </p>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-xl bg-red-500/10 flex items-center justify-center">
              <TrendingDown className="w-5 h-5 text-red-400" />
            </div>
            <div>
              <p className="text-xs text-[var(--color-text-secondary)]">Top Losers</p>
              <p className="text-lg font-bold text-red-400">
                {losers[0]?.symbol ?? "—"}
              </p>
            </div>
          </div>
          <p className="text-sm text-red-400 font-semibold">
            {losers[0]?.change_percent?.toFixed(2) ?? 0}%
          </p>
        </div>

        <div className="glass-card p-5">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 flex items-center justify-center">
              <BarChart3 className="w-5 h-5 text-indigo-400" />
            </div>
            <div>
              <p className="text-xs text-[var(--color-text-secondary)]">Most Active</p>
              <p className="text-lg font-bold text-indigo-400">
                {mostActive[0]?.symbol ?? "—"}
              </p>
            </div>
          </div>
          <p className="text-sm text-[var(--color-text-secondary)]">
            Vol: {formatVolume(mostActive[0]?.volume ?? 0)}
          </p>
        </div>
      </div>

      {/* Stock Table */}
      <div className="glass-card overflow-hidden">
        <div className="px-5 py-4 border-b border-[var(--color-border)]">
          <h3 className="text-sm font-semibold text-[var(--color-text-secondary)] uppercase tracking-wider">
            All Stocks
          </h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-[var(--color-border)]">
                <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase">
                  Symbol
                </th>
                <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase hidden sm:table-cell">
                  Name
                </th>
                <th className="text-left px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase hidden md:table-cell">
                  Sector
                </th>
                <th className="text-right px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase">
                  Price
                </th>
                <th className="text-right px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase">
                  Change
                </th>
                <th className="text-right px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase hidden sm:table-cell">
                  Volume
                </th>
                <th className="px-5 py-3" />
              </tr>
            </thead>
            <tbody>
              {stocks.map((stock, i) => (
                <tr
                  key={stock.symbol}
                  className="border-b border-[var(--color-border)]/50 hover:bg-white/[0.02] transition-colors animate-fade-in"
                  style={{ animationDelay: `${i * 30}ms` }}
                >
                  <td className="px-5 py-3">
                    <span className="font-semibold text-[var(--color-text-primary)]">
                      {stock.symbol}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-sm text-[var(--color-text-secondary)] hidden sm:table-cell">
                    {stock.name}
                  </td>
                  <td className="px-5 py-3 hidden md:table-cell">
                    <span className="text-xs px-2 py-1 rounded-full bg-[var(--color-surface-elevated)] text-[var(--color-text-secondary)]">
                      {stock.sector}
                    </span>
                  </td>
                  <td className="px-5 py-3 text-right font-mono text-sm">
                    {stock.last_price.toFixed(2)}
                  </td>
                  <td className={`px-5 py-3 text-right text-sm font-semibold ${getChangeColor(stock.change)}`}>
                    <div className="flex items-center justify-end gap-1">
                      {stock.change > 0 ? (
                        <TrendingUp className="w-3 h-3" />
                      ) : stock.change < 0 ? (
                        <TrendingDown className="w-3 h-3" />
                      ) : null}
                      {stock.change > 0 ? "+" : ""}
                      {stock.change_percent.toFixed(2)}%
                    </div>
                  </td>
                  <td className="px-5 py-3 text-right text-sm text-[var(--color-text-secondary)] font-mono hidden sm:table-cell">
                    {formatVolume(stock.volume)}
                  </td>
                  <td className="px-5 py-3 text-right">
                    <Link
                      href={`/stocks/${stock.symbol}`}
                      className="inline-flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
                    >
                      Analyze <ArrowRight className="w-3 h-3" />
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
