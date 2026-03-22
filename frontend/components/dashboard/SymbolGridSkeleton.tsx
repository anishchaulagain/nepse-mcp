import { Search } from "lucide-react";

export default function SymbolGridSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
         <div className="h-7 w-48 bg-[var(--color-surface-elevated)] rounded-md opacity-50" />
         <div className="relative w-full sm:w-72">
           <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[var(--color-text-secondary)] opacity-50" />
           <div className="w-full h-10 bg-[var(--color-surface-elevated)] border border-[var(--color-border)] rounded-xl opacity-50" />
         </div>
      </div>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
        {Array.from({ length: 48 }).map((_, i) => (
          <div
            key={i}
            className="glass-card p-3 flex flex-col justify-between h-[80px] bg-[var(--color-surface-elevated)] opacity-20"
            style={{ animationDelay: `${(i % 10) * 100}ms` }}
          >
            <div className="flex justify-between items-start mb-2">
              <div className="h-4 w-12 bg-white/20 rounded-md" />
              <div className="w-3.5 h-3.5 bg-white/10 rounded-full" />
            </div>
            <div className="space-y-1">
              <div className="h-2 w-full bg-white/10 rounded-md" />
              <div className="h-2 w-2/3 bg-white/10 rounded-md" />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
