"use client";

import { Mission } from "@/lib/types";
import { Zap, ShieldCheck, Target, Layers, FileDown, CheckCircle } from "lucide-react";

interface MissionImpactProps {
  mission: Mission;
  onExportFHIR?: () => void;
}

export function MissionImpact({ mission, onExportFHIR }: MissionImpactProps) {
  return (
    <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-6 font-mono shadow-2xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 text-emerald-400">
          <Target className="h-4 w-4" />
          <span className="text-xs font-bold uppercase tracking-wider">
            PROJECTED CAMPAIGN IMPACT & YIELD
          </span>
        </div>
        <span className="text-[10px] text-slate-500 uppercase">
          BAYESIAN UNCERTAINTY DECAY MODEL
        </span>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
          <div className="flex items-center justify-between text-[10px] text-slate-500 uppercase">
            <span>Expected Info Gain</span>
            <Zap className="h-3.5 w-3.5 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400">
            +{(mission.expectedInformationGain * 100).toFixed(0)}%
          </div>
          <div className="text-[10px] text-slate-400">Entropy reduction across reach</div>
        </div>

        <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
          <div className="flex items-center justify-between text-[10px] text-slate-500 uppercase">
            <span>Coverage Improvement</span>
            <Layers className="h-3.5 w-3.5 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-cyan-400">
            +{mission.coverageImprovement}%
          </div>
          <div className="text-[10px] text-slate-400">Reach spatial density increase</div>
        </div>

        <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
          <div className="flex items-center justify-between text-[10px] text-slate-500 uppercase">
            <span>Critical Gaps Targeted</span>
            <ShieldCheck className="h-3.5 w-3.5 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-400">
            {mission.knowledgeGapsAddressed?.length || 0} GAPS
          </div>
          <div className="text-[10px] text-slate-400">High-leverage missing metrics</div>
        </div>
      </div>

      {/* Knowledge Gaps Targeted */}
      <div className="space-y-3">
        <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
          <Target className="h-3 w-3 text-cyan-400" />
          <span>KNOWLEDGE GAPS RESOLVED BY THIS CAMPAIGN</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {mission.knowledgeGapsAddressed?.map((gap, i) => (
            <div
              key={i}
              className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800/80 flex items-start gap-2.5 text-xs text-slate-200"
            >
              <CheckCircle className="h-4 w-4 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <div className="font-semibold text-[11px] text-slate-100">{gap}</div>
                <div className="text-[10px] text-slate-500">Uncertainty resolution: High</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="pt-2 flex flex-col sm:flex-row items-center gap-3">
        {onExportFHIR && (
          <button
            onClick={onExportFHIR}
            className="w-full sm:w-auto flex-1 py-2.5 px-4 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 font-bold text-xs uppercase tracking-wider flex items-center justify-center gap-2 transition-all"
          >
            <FileDown className="h-4 w-4 text-cyan-400" />
            <span>EXPORT DISPATCH AS FHIR BUNDLE</span>
          </button>
        )}
      </div>
    </div>
  );
}
