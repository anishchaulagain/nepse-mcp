import SymbolGrid from "./SymbolGrid";
import { getStocks } from "@/lib/api";
import { Activity } from "lucide-react";

export default async function SymbolGridWrapper() {
  try {
    const data = await getStocks();
    
    if (!data.stocks || data.stocks.length === 0) {
      return (
        <div className="glass-card p-12 text-center">
          <Activity className="w-12 h-12 text-[var(--color-text-secondary)] mx-auto mb-4 opacity-50" />
          <h3 className="text-lg font-semibold text-[var(--color-text-primary)] mb-2">
            No market data available.
          </h3>
          <p className="text-sm text-[var(--color-text-secondary)]">
            Could not retrieve symbols from the server.
          </p>
        </div>
      );
    }

    return <SymbolGrid stocks={data.stocks} />;
  } catch (error: any) {
    return (
      <div className="glass-card p-6 border border-red-500/30 bg-red-500/5">
        <p className="text-red-400 text-sm">
          ⚠️ Failed to fetch markets — {error.message || "Ensure backend is running on port 8000."}
        </p>
      </div>
    );
  }
}
