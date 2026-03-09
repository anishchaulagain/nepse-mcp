import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPrice(price: number): string {
  return `NPR ${price.toLocaleString("en-NP", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

export function formatVolume(vol: number): string {
  if (vol >= 1_000_000) return `${(vol / 1_000_000).toFixed(1)}M`;
  if (vol >= 1_000) return `${(vol / 1_000).toFixed(1)}K`;
  return vol.toString();
}

export function getTrendColor(trend: string): string {
  const map: Record<string, string> = {
    bullish: "text-emerald-400",
    bearish: "text-red-400",
    sideways: "text-amber-400",
    overbought: "text-orange-400",
    oversold: "text-cyan-400",
    breakout_possible: "text-violet-400",
    bullish_crossover: "text-emerald-400",
    bearish_crossover: "text-red-400",
  };
  return map[trend] || "text-gray-400";
}

export function getTrendBg(trend: string): string {
  const map: Record<string, string> = {
    bullish: "bg-emerald-500/10 border-emerald-500/30",
    bearish: "bg-red-500/10 border-red-500/30",
    sideways: "bg-amber-500/10 border-amber-500/30",
    overbought: "bg-orange-500/10 border-orange-500/30",
    oversold: "bg-cyan-500/10 border-cyan-500/30",
    breakout_possible: "bg-violet-500/10 border-violet-500/30",
  };
  return map[trend] || "bg-gray-500/10 border-gray-500/30";
}

export function getChangeColor(change: number): string {
  if (change > 0) return "text-emerald-400";
  if (change < 0) return "text-red-400";
  return "text-gray-400";
}
