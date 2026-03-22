"use client";

import { useState } from "react";
import Link from "next/link";
import { StockInfo } from "@/types";
import { Search, ArrowRight, TrendingUp, TrendingDown, Activity } from "lucide-react";
import { formatVolume, getChangeColor } from "@/lib/utils";

export default function SymbolGrid({ stocks }: { stocks: StockInfo[] }) {
  const [query, setQuery] = useState("");
  const [minPrice, setMinPrice] = useState<string>("");
  const [maxPrice, setMaxPrice] = useState<string>("");
  
  const filteredStocks = stocks.filter((s) => {
    const matchesQuery = s.symbol.toLowerCase().includes(query.toLowerCase()) || 
                         s.name.toLowerCase().includes(query.toLowerCase());
    const passMin = minPrice ? s.last_price >= parseFloat(minPrice) : true;
    const passMax = maxPrice ? s.last_price <= parseFloat(maxPrice) : true;
    return matchesQuery && passMin && passMax;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col lg:flex-row gap-4 lg:items-center justify-between">
         <h2 className="text-xl font-bold gradient-text">Available Markets</h2>
         <div className="flex flex-col sm:flex-row gap-3">
           <div className="relative w-full sm:w-64">
             <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-text-secondary)]" />
             <input
               type="text"
               placeholder="Filter by symbol or name..."
               value={query}
               onChange={(e) => setQuery(e.target.value)}
               className="w-full bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-indigo-500/50 transition-colors"
             />
           </div>
           <div className="flex items-center gap-2 w-full sm:w-auto">
             <input
               type="number"
               placeholder="Min Price"
               value={minPrice}
               onChange={(e) => setMinPrice(e.target.value)}
               className="w-full sm:w-28 bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl py-2 px-3 text-sm focus:outline-none focus:border-indigo-500/50 transition-colors"
             />
             <span className="text-[var(--color-text-secondary)]">-</span>
             <input
               type="number"
               placeholder="Max Price"
               value={maxPrice}
               onChange={(e) => setMaxPrice(e.target.value)}
               className="w-full sm:w-28 bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl py-2 px-3 text-sm focus:outline-none focus:border-indigo-500/50 transition-colors"
             />
           </div>
         </div>
      </div>
      
      <div className="glass-card overflow-hidden">
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
                <th className="text-right px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase hidden lg:table-cell">
                  Open
                </th>
                <th className="text-right px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase hidden lg:table-cell">
                  High
                </th>
                <th className="text-right px-5 py-3 text-xs font-medium text-[var(--color-text-secondary)] uppercase hidden lg:table-cell">
                  Low
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
              {filteredStocks.map((stock, i) => (
                <tr
                  key={stock.symbol}
                  className="border-b border-[var(--color-border)]/50 hover:bg-white/[0.02] transition-colors animate-fade-in"
                  style={{ animationDelay: `${Math.min(i * 10, 500)}ms` }}
                >
                  <td className="px-5 py-3">
                    <Link href={`/stocks/${stock.symbol}`} className="font-semibold text-indigo-400 hover:text-indigo-300 transition-colors">
                      {stock.symbol}
                    </Link>
                  </td>
                  <td className="px-5 py-3 text-sm text-[var(--color-text-secondary)] hidden sm:table-cell">
                    {stock.name}
                  </td>
                  <td className="px-5 py-3 text-right font-mono text-sm text-[var(--color-text-secondary)] hidden lg:table-cell">
                    {stock.opening_price?.toFixed(2) || "—"}
                  </td>
                  <td className="px-5 py-3 text-right font-mono text-sm text-[var(--color-text-secondary)] hidden lg:table-cell">
                    {stock.max_price?.toFixed(2) || "—"}
                  </td>
                  <td className="px-5 py-3 text-right font-mono text-sm text-[var(--color-text-secondary)] hidden lg:table-cell">
                    {stock.min_price?.toFixed(2) || "—"}
                  </td>
                  <td className="px-5 py-3 text-right font-mono text-sm font-medium text-[var(--color-text-primary)]">
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
              {filteredStocks.length === 0 && (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-[var(--color-text-secondary)] text-sm">
                    <Activity className="w-8 h-8 mx-auto mb-3 opacity-20" />
                    No markets found properly matching criteria.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
