"use client";

import { motion } from "motion/react";

interface EvidenceMetricProps {
  label: string;
  value: number;
  description?: string;
  delay?: number;
}

export function EvidenceMetric({ label, value, description, delay = 0 }: EvidenceMetricProps) {
  const getQualityColor = (val: number) => {
    if (val >= 90) return "text-emerald-400";
    if (val >= 75) return "text-cyan-400";
    if (val >= 50) return "text-amber-400";
    return "text-rose-400";
  };

  const getBarColor = (val: number) => {
    if (val >= 90) return "from-emerald-500 to-teal-400";
    if (val >= 75) return "from-cyan-500 to-blue-500";
    if (val >= 50) return "from-amber-500 to-yellow-400";
    return "from-rose-500 to-red-600";
  };

  return (
    <div className="space-y-1.5 p-3 rounded-lg bg-slate-950/40 border border-slate-800/80 hover:border-slate-700/80 transition-colors">
      <div className="flex items-center justify-between text-xs font-mono">
        <span className="text-slate-300">{label}</span>
        <span className={`font-bold ${getQualityColor(value)}`}>{value}%</span>
      </div>
      <div className="w-full h-1.5 bg-slate-900 rounded-full overflow-hidden border border-slate-800/50">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ duration: 0.8, delay }}
          className={`h-full bg-gradient-to-r ${getBarColor(value)} rounded-full`}
        />
      </div>
      {description && (
        <div className="text-[10px] text-slate-500 font-mono leading-tight">{description}</div>
      )}
    </div>
  );
}
