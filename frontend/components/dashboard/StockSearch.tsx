"use client";

import { Zap } from "lucide-react";
import { useRouter } from "next/navigation";

export default function StockSearch() {
  const router = useRouter();

  const handleSearch = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const symbol = formData.get("symbol")?.toString().trim().toUpperCase();
    if (symbol) {
      router.push(`/stocks/${symbol}`);
    }
  };

  return (
    <div className="mb-8 animate-slide-up" style={{ animationDelay: "50ms" }}>
      <form onSubmit={handleSearch} className="relative max-w-xl">
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
  );
}
