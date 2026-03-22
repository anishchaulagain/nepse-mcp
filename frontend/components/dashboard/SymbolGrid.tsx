"use client";

import { useState } from "react";
import Link from "next/link";
import { StockInfo } from "@/types";
import { Search, Activity } from "lucide-react";

export default function SymbolGrid({ stocks }: { stocks: StockInfo[] }) {
  const [query, setQuery] = useState("");
  
  const filteredStocks = stocks.filter(
    (s) =>
      s.symbol.toLowerCase().includes(query.toLowerCase()) ||
      s.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
         <h2 className="text-xl font-bold gradient-text">Available Markets</h2>
         <div className="relative w-full sm:w-72">
           <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-text-secondary)]" />
           <input
             type="text"
             placeholder="Filter by symbol or name..."
             value={query}
             onChange={(e) => setQuery(e.target.value)}
             className="w-full bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl py-2 pl-10 pr-4 text-sm focus:outline-none focus:border-indigo-500/50 transition-colors"
           />
         </div>
      </div>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
        {filteredStocks.map((stock, i) => (
          <Link
            href={`/stocks/${stock.symbol}`}
            key={stock.symbol}
            className="glass-card p-3 flex flex-col justify-between hover:border-indigo-500/40 hover:bg-white/[0.03] transition-all group animate-fade-in"
            style={{ animationDelay: `${Math.min(i * 10, 500)}ms` }}
          >
            <div className="flex justify-between items-start mb-2">
              <span className="font-bold text-[var(--color-text-primary)] text-sm group-hover:text-indigo-300 transition-colors">
                {stock.symbol}
              </span>
              <Activity className="w-3.5 h-3.5 text-[var(--color-text-secondary)] group-hover:text-indigo-400 transition-colors mt-0.5" />
            </div>
            <p className="text-[10px] text-[var(--color-text-secondary)] line-clamp-2 leading-tight">
              {stock.name}
            </p>
          </Link>
        ))}
        {filteredStocks.length === 0 && (
          <div className="col-span-full py-12 text-center text-[var(--color-text-secondary)] text-sm bg-[var(--color-surface-elevated)] rounded-xl border border-[var(--color-border)]">
            <Search className="w-8 h-8 mx-auto mb-3 opacity-20" />
            No markets found matching "{query}"
          </div>
        )}
      </div>
    </div>
  );
}
