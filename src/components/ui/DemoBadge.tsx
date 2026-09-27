"use client";

import { Activity } from "lucide-react";

export function DemoBadge() {
  return (
    <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-cyan-950/40 border border-cyan-500/30 text-cyan-400 text-xs font-mono tracking-wider">
      <span className="relative flex h-1.5 w-1.5">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
        <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-cyan-500"></span>
      </span>
      <span className="text-[11px] uppercase">DEMO SNAPSHOT</span>
    </div>
  );
}
