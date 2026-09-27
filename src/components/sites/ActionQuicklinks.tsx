"use client";

import Link from "next/link";
import { ChevronRight, ShieldCheck, Copy, Sparkles, Send } from "lucide-react";

export function ActionQuicklinks({ siteId }: { siteId: string }) {
  const links = [
    { href: `/trust?siteId=${siteId}`, label: "Evidence X-RAY", icon: ShieldCheck, color: "text-blue-400" },
    { href: `/twins?siteId=${siteId}`, label: "Find Twins", icon: Copy, color: "text-indigo-400" },
    { href: `/oracle?siteId=${siteId}`, label: "Ask Oracle", icon: Sparkles, color: "text-emerald-400" }
  ];

  return (
    <div className="space-y-3">
      {links.map((l) => (
        <Link
          key={l.href}
          href={l.href}
          className="w-full p-3 rounded-lg bg-slate-900/60 border border-slate-800 hover:border-slate-600 text-slate-200 font-mono text-xs transition-all flex items-center justify-between group"
        >
          <div className="flex items-center gap-3">
            <l.icon className={`h-4 w-4 ${l.color}`} />
            <span>{l.label}</span>
          </div>
          <ChevronRight className="h-4 w-4 text-slate-500 group-hover:text-slate-300 group-hover:translate-x-0.5 transition-all" />
        </Link>
      ))}
      <Link
        href={`/missions?siteId=${siteId}`}
        className="w-full mt-4 p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/30 hover:bg-emerald-500/20 text-emerald-400 font-mono text-xs font-bold transition-all flex items-center justify-between group"
      >
        <div className="flex items-center gap-3">
          <Send className="h-4 w-4" />
          <span>Plan Mission</span>
        </div>
        <ChevronRight className="h-4 w-4 group-hover:translate-x-0.5 transition-all" />
      </Link>
    </div>
  );
}
