"use client";

import { EvidenceFlag as EvidenceFlagType } from "@/lib/types";
import { CheckCircle2, AlertTriangle, AlertCircle, Info } from "lucide-react";

interface EvidenceFlagProps {
  flag: EvidenceFlagType;
}

export function EvidenceFlagItem({ flag }: EvidenceFlagProps) {
  const getIconAndColor = (status: EvidenceFlagType["status"]) => {
    switch (status) {
      case "complete":
        return {
          icon: CheckCircle2,
          color: "text-emerald-400 border-emerald-900/40 bg-emerald-950/20",
          label: "VERIFIED"
        };
      case "partial":
        return {
          icon: Info,
          color: "text-cyan-400 border-cyan-900/40 bg-cyan-950/20",
          label: "SUFFICIENT"
        };
      case "warning":
        return {
          icon: AlertTriangle,
          color: "text-amber-400 border-amber-900/40 bg-amber-950/20",
          label: "DEGRADED"
        };
      case "critical":
        return {
          icon: AlertCircle,
          color: "text-rose-400 border-rose-900/40 bg-rose-950/20",
          label: "CRITICAL"
        };
    }
  };

  const { icon: Icon, color, label } = getIconAndColor(flag.status);

  return (
    <div className={`p-3 rounded-lg border flex items-center justify-between font-mono text-xs ${color}`}>
      <div className="flex items-center gap-2.5">
        <Icon className="h-4 w-4 shrink-0" />
        <span className="capitalize">{flag.metric.replace(/([A-Z])/g, " $1")}</span>
      </div>
      <div className="flex items-center gap-3">
        <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-900/80 border border-slate-700/60 text-slate-300">
          {label}
        </span>
        <span className="font-bold">{flag.score}%</span>
      </div>
    </div>
  );
}
