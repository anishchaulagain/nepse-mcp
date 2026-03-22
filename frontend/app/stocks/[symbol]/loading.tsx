import { Activity } from "lucide-react";

export default function StockAnalysisLoading() {
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 animate-pulse">
      {/* Header Skeleton */}
      <div className="flex items-center gap-4 mb-6">
        <div className="w-10 h-10 rounded-lg bg-[var(--color-surface-elevated)] border border-[var(--color-border)] opacity-60" />
        <div className="space-y-2">
          <div className="h-8 w-32 bg-[var(--color-surface-elevated)] rounded-md opacity-60" />
          <div className="h-4 w-20 bg-[var(--color-surface-elevated)] rounded-md opacity-40" />
        </div>
        <div className="ml-auto flex items-center gap-2 px-4 py-2 glass-card border-indigo-500/30 bg-indigo-500/5">
           <Activity className="w-4 h-4 text-indigo-400 animate-spin-slow" />
           <span className="text-sm font-semibold text-indigo-400">Running AI Models...</span>
        </div>
      </div>

      <div className="space-y-6">
        {/* Chart Skeleton */}
        <div className="glass-card h-[500px] w-full p-4 flex flex-col justify-between opacity-50">
           <div className="flex justify-between items-center mb-4">
              <div className="flex gap-2">
                 <div className="w-16 h-6 bg-[var(--color-surface-elevated)] rounded-md" />
                 <div className="w-16 h-6 bg-[var(--color-surface-elevated)] rounded-md" />
                 <div className="w-16 h-6 bg-[var(--color-surface-elevated)] rounded-md" />
              </div>
              <div className="w-32 h-6 bg-[var(--color-surface-elevated)] rounded-md" />
           </div>
           
           {/* Fake chart lines/bars */}
           <div className="flex-1 border-t border-b border-[var(--color-border)] flex items-end justify-between px-2 pb-4 gap-2">
              {Array.from({ length: 40 }).map((_, i) => (
                <div 
                  key={i} 
                  className="w-full bg-[var(--color-surface-elevated)] rounded-t-sm"
                  style={{ 
                    height: `${20 + Math.random() * 60}%`,
                    opacity: 0.1 + Math.random() * 0.4
                  }}
                />
              ))}
           </div>
        </div>

        {/* Indicators + Prediction Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Indicator Panel Skeleton */}
          <div className="glass-card p-5 space-y-4 opacity-50">
             <div className="h-6 w-48 bg-[var(--color-surface-elevated)] rounded-md mb-6" />
             <div className="grid grid-cols-2 gap-4">
               {Array.from({ length: 6 }).map((_, i) => (
                  <div key={i} className="h-16 w-full bg-[var(--color-surface-elevated)] rounded-lg" />
               ))}
             </div>
          </div>

          {/* AI Prediction Card Skeleton */}
          <div className="space-y-4 opacity-50">
            <div className="glass-card p-5">
              <div className="flex justify-between items-start mb-6">
                <div className="space-y-2">
                  <div className="h-4 w-24 bg-[var(--color-surface-elevated)] rounded-md" />
                  <div className="h-8 w-32 bg-[var(--color-surface-elevated)] rounded-md" />
                </div>
                <div className="w-16 h-16 rounded-full border-4 border-[var(--color-surface-elevated)]" />
              </div>
              <div className="space-y-2 mt-4">
                <div className="h-4 w-full bg-[var(--color-surface-elevated)] rounded-md" />
                <div className="h-4 w-3/4 bg-[var(--color-surface-elevated)] rounded-md" />
              </div>
            </div>

            <div className="glass-card p-5 space-y-3">
              <div className="flex justify-between items-center mb-2">
                <div className="h-5 w-32 bg-[var(--color-surface-elevated)] rounded-md" />
                <div className="h-6 w-20 rounded-full bg-[var(--color-surface-elevated)]" />
              </div>
              <div className="h-3 w-full bg-[var(--color-surface-elevated)] rounded-md" />
              <div className="h-3 w-full bg-[var(--color-surface-elevated)] rounded-md" />
              <div className="h-3 w-5/6 bg-[var(--color-surface-elevated)] rounded-md" />
              <div className="h-3 w-4/6 bg-[var(--color-surface-elevated)] rounded-md" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
