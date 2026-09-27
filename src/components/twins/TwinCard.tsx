"use client";

import { TwinMatch } from "@/lib/types";
import { GitCompare, ShieldCheck, Clock } from "lucide-react";
import { motion } from "motion/react";

interface TwinCardProps {
  twin: TwinMatch;
  isSelected?: boolean;
  onSelect: () => void;
}

export function TwinCard({ twin, isSelected, onSelect }: TwinCardProps) {
  const signalLabels = [
    { label: "Water Profile", strength: twin.matchSignals.waterProfile },
    { label: "Habitat Profile", strength: twin.matchSignals.habitatProfile },
    { label: "EO Context", strength: twin.matchSignals.eoContext },
    { label: "Temporal Overlap", strength: twin.matchSignals.temporalOverlap }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`p-5 rounded-xl font-mono transition-all border ${
        isSelected
          ? "bg-cyan-950/30 border-cyan-500 shadow-lg shadow-cyan-950/50"
          : "bg-slate-900/50 border-slate-800 hover:border-slate-700 hover:bg-slate-900/80"
      }`}
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-cyan-400 font-bold border border-slate-700">
              {twin.siteCode}
            </span>
          </div>
          <h3 className="text-base font-bold text-slate-100 mt-1 uppercase tracking-tight">
            {twin.siteName}
          </h3>
        </div>

        <div className="text-right">
          <div className="text-2xl font-bold text-emerald-400 font-mono">
            {twin.similarity}%
          </div>
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">
            ECOLOGICAL SIMILARITY
          </div>
        </div>
      </div>

      {/* Sub metrics */}
      <div className="grid grid-cols-2 gap-3 my-4 pt-3 border-t border-slate-800/80 text-xs">
        <div className="p-2 rounded bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
          <span className="text-[10px] text-slate-500 uppercase flex items-center gap-1">
            <ShieldCheck className="h-3 w-3 text-emerald-400" /> CONFIDENCE
          </span>
          <span className="font-bold text-slate-200">{twin.evidenceConfidence}%</span>
        </div>
        <div className="p-2 rounded bg-slate-950/60 border border-slate-800/80 flex items-center justify-between">
          <span className="text-[10px] text-slate-500 uppercase flex items-center gap-1">
            <Clock className="h-3 w-3 text-cyan-400" /> TEMPORAL ALIGN
          </span>
          <span className="font-bold text-slate-200">{twin.temporalAlignment}%</span>
        </div>
      </div>

      {/* Matching Signals */}
      <div className="space-y-1.5 mb-4">
        <div className="text-[10px] text-slate-500 uppercase tracking-wider">
          Shared Ecological Dimensions
        </div>
        <div className="flex flex-wrap gap-1.5">
          {signalLabels.map((sig, i) => (
            <span
              key={i}
              className={`text-[10px] px-2 py-0.5 rounded border flex items-center gap-1 ${
                sig.strength === "strong"
                  ? "bg-emerald-950/40 text-emerald-400 border-emerald-800/50"
                  : sig.strength === "moderate"
                  ? "bg-cyan-950/40 text-cyan-300 border-cyan-800/50"
                  : "bg-slate-800/60 text-slate-400 border-slate-700/50"
              }`}
            >
              <span
                className={`h-1 w-1 rounded-full ${
                  sig.strength === "strong"
                    ? "bg-emerald-400"
                    : sig.strength === "moderate"
                    ? "bg-cyan-400"
                    : "bg-slate-500"
                }`}
              />
              {sig.label}: {sig.strength.toUpperCase()}
            </span>
          ))}
        </div>
      </div>

      <button
        onClick={onSelect}
        className={`w-full py-2 px-3 rounded text-xs font-bold uppercase tracking-wider flex items-center justify-center gap-2 transition-colors ${
          isSelected
            ? "bg-cyan-500 text-slate-950 hover:bg-cyan-400"
            : "bg-slate-800 text-slate-200 hover:bg-slate-700 border border-slate-700"
        }`}
      >
        <GitCompare className="h-3.5 w-3.5" />
        <span>{isSelected ? "VIEWING COMPARISON" : "COMPARE WITH TWIN"}</span>
      </button>
    </motion.div>
  );
}
