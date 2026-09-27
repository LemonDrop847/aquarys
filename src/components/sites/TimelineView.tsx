"use client";

import { motion } from "motion/react";

export function Timeline({ siteId }: { siteId: string }) {
  const events = [
    { date: "2023-01", label: "Baseline", val: 65 },
    { date: "2023-06", label: "Survey", val: 72 },
    { date: "2024-01", label: "EO Pass", val: 78 },
    { date: "2024-06", label: "Current", val: 82 }
  ];

  return (
    <div className="space-y-4">
      <div className="text-xs text-slate-400 font-mono uppercase tracking-wider mb-4">
        Observation Timeline
      </div>
      <div className="relative flex justify-between items-end h-24 pb-6 px-2">
        <div className="absolute bottom-6 left-2 right-2 h-px bg-slate-800" />
        {events.map((ev, i) => (
          <motion.div
            key={ev.date}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.15 }}
            className="relative flex flex-col items-center gap-2 group cursor-crosshair"
          >
            <div className="text-[10px] text-cyan-400 font-mono opacity-0 group-hover:opacity-100 transition-opacity absolute -top-6 whitespace-nowrap">
              Score: {ev.val}
            </div>
            <div className="w-3 h-3 rounded-full bg-slate-900 border-2 border-cyan-500 z-10 shadow-[0_0_8px_rgba(6,182,212,0.5)] group-hover:bg-cyan-400 transition-colors" />
            <div className="text-[10px] font-mono text-slate-400 absolute -bottom-5 whitespace-nowrap">
              {ev.date}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
