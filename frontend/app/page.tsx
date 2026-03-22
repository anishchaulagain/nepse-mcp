import { Suspense } from "react";
import SymbolGridWrapper from "@/components/dashboard/SymbolGridWrapper";
import SymbolGridSkeleton from "@/components/dashboard/SymbolGridSkeleton";
import { Activity, TrendingUp, Zap } from "lucide-react";
import StockSearch from "@/components/dashboard/StockSearch";

export const dynamic = "force-dynamic";

export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      {/* Hero */}
      <div className="mb-8 animate-slide-up">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center shadow-lg shadow-indigo-500/20">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-3xl font-extrabold gradient-text">NEPSE AI Dashboard</h1>
            <p className="text-sm text-[var(--color-text-secondary)]">
              AI-powered market analysis & predictions
            </p>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      <StockSearch />

      {/* Quick Actions */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mb-8 animate-slide-up" style={{ animationDelay: "100ms" }}>
        <a
          href="/stocks/NABIL"
          className="glass-card p-4 flex items-center gap-3 group hover:border-emerald-500/30 transition-all"
        >
          <TrendingUp className="w-5 h-5 text-emerald-400 group-hover:scale-110 transition-transform" />
          <div>
            <p className="text-sm font-semibold text-[var(--color-text-primary)]">Analyze NABIL</p>
            <p className="text-xs text-[var(--color-text-secondary)]">Full AI analysis with charts</p>
          </div>
        </a>
        <a
          href="/stocks/NICA"
          className="glass-card p-4 flex items-center gap-3 group hover:border-violet-500/30 transition-all"
        >
          <Zap className="w-5 h-5 text-violet-400 group-hover:scale-110 transition-transform" />
          <div>
            <p className="text-sm font-semibold text-[var(--color-text-primary)]">Analyze NICA</p>
            <p className="text-xs text-[var(--color-text-secondary)]">Breakout detection & indicators</p>
          </div>
        </a>
      </div>

      {/* Symbol Grid */}
      <Suspense fallback={<SymbolGridSkeleton />}>
        <SymbolGridWrapper />
      </Suspense>
    </div>
  );
}
