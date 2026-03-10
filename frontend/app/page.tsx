import { getStocks } from "@/lib/api";
import MarketOverview from "@/components/dashboard/MarketOverview";
import { Activity, TrendingUp, Zap } from "lucide-react";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  let stocks: any[] = [];
  let error = "";

  try {
    const data = await getStocks();
    stocks = data.stocks;
  } catch (e: any) {
    error = e.message || "Failed to fetch stocks";
  }

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
      <div className="mb-8 animate-slide-up" style={{ animationDelay: "50ms" }}>
        <form 
          onSubmit={(e) => {
            e.preventDefault();
            const formData = new FormData(e.currentTarget);
            const symbol = formData.get("symbol")?.toString().trim().toUpperCase();
            if (symbol) window.location.href = `/stocks/${symbol}`;
          }}
          className="relative max-w-xl"
        >
          <input
            type="text"
            name="symbol"
            placeholder="Search stock symbol (e.g. NABIL, NTC, HIDCL)..."
            className="w-full bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl py-4 px-6 pr-12 text-[var(--color-text-primary)] focus:outline-none focus:ring-2 focus:ring-indigo-500/50 focus:border-indigo-500 transition-all shadow-lg"
          />
          <button 
            type="submit"
            className="absolute right-4 top-1/2 -translate-y-1/2 p-2 text-[var(--color-text-secondary)] hover:text-indigo-400 transition-colors"
          >
            <Zap className="w-5 h-5" />
          </button>
        </form>
      </div>

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

      {/* Error State */}
      {error && (
        <div className="glass-card p-6 mb-6 border border-red-500/30 bg-red-500/5">
          <p className="text-red-400 text-sm">
            ⚠️ {error} — Make sure the backend is running on port 8000.
          </p>
        </div>
      )}

      {/* Market Overview */}
      {stocks.length > 0 && <MarketOverview stocks={stocks} />}

      {/* Empty State */}
      {!error && stocks.length === 0 && (
        <div className="glass-card p-12 text-center">
          <Activity className="w-12 h-12 text-[var(--color-text-secondary)] mx-auto mb-4" />
          <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2">
            Loading market data...
          </h3>
          <p className="text-sm text-[var(--color-text-secondary)]">
            Connecting to NEPSE AI backend
          </p>
        </div>
      )}
    </div>
  );
}
