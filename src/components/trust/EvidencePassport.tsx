"use client";

import { EvidenceProfile } from "@/lib/types";
import { EvidenceMetric } from "./EvidenceMetric";
import { TrustExplanation } from "./TrustExplanation";
import { EvidenceFlagItem } from "./EvidenceFlag";
import { motion } from "motion/react";
import { FileDown, GitGraph, RotateCw } from "lucide-react";

interface EvidencePassportProps {
  profile: EvidenceProfile;
  onExport: () => void;
  onViewGraph: () => void;
  onReScan: () => void;
}

export function EvidencePassport({ profile, onExport, onViewGraph, onReScan }: EvidencePassportProps) {
  const metrics = [
    { label: "Completeness", value: profile.completeness },
    { label: "Consistency", value: profile.consistency },
    { label: "Location", value: profile.location },
    { label: "Temporal Validity", value: profile.temporalValidity },
    { label: "Image Support", value: profile.imageSupport },
    { label: "Cross-Observer", value: profile.crossObserver },
    { label: "Independent", value: profile.independentSupport }
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-mono uppercase tracking-wider text-slate-200">
          EVIDENCE PASSPORT // {profile.observationId}
        </h2>
        <div className="flex items-center gap-2">
          <button onClick={onReScan} className="text-xs p-2 rounded bg-slate-900 border border-slate-700 hover:border-slate-500 text-slate-300">
            <RotateCw className="h-3.5 w-3.5" />
          </button>
          <button onClick={onViewGraph} className="text-xs p-2 rounded bg-slate-900 border border-slate-700 hover:border-slate-500 text-slate-300">
            <GitGraph className="h-3.5 w-3.5" />
          </button>
          <button onClick={onExport} className="text-xs p-2 rounded bg-emerald-950/30 border border-emerald-900 hover:border-emerald-700 text-emerald-400">
            <FileDown className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {metrics.map((m, i) => (
              <EvidenceMetric key={m.label} {...m} delay={i * 0.05} />
            ))}
          </div>

          <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 space-y-3">
             <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider">Integrity Flags</div>
             {profile.flags.map((flag, i) => (
               <EvidenceFlagItem key={i} flag={flag} />
             ))}
          </div>
        </div>

        <div className="space-y-6">
          <TrustExplanation explanation={profile.explanation} warnings={profile.warnings} />
        </div>
      </div>
    </div>
  );
}
