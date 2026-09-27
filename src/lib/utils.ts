import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatPercentage(val: number): string {
  return `${Math.round(val * 100)}%`;
}

export function formatScore(val: number): string {
  return `${Math.round(val)}%`;
}

export function truncateText(str: string, maxLen: number = 60): string {
  if (str.length <= maxLen) return str;
  return str.slice(0, maxLen) + "...";
}
