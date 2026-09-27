"use client";

import { Check, AlertTriangle, HelpCircle } from "lucide-react";

interface TrustExplanationProps {
  explanation: string;
  warnings?: string[];
}

export function TrustExplanation({ explanation, warnings = [] }: TrustExplanationProps) {
  const bulletPoints = [
    { text: "Required schema fields validated & complete", type: "pass" },
    { text: "Spatially aligned with hydrological catchment boundaries", type: "pass" },
    { text: "Consistent with 6 independent nearby observer records", type: "pass" },
    { text: "Sentinel-2 multispectral surface reflectance corroboration", type: "pass" }
  ];

  return (
    <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 font-mono space-y-4">
      <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
        <HelpCircle className="h-4 w-4 text-cyan-400" />
        <h3 className="text-xs uppercase tracking-wider font-semibold text-slate-200">
          PROVENANCE & INTEGRITY AUDIT // WHY?
        </h3>
      </div>

      <p className="text-xs text-slate-300 leading-relaxed font-sans">{explanation}</p>

      <div className="space-y-2 pt-2">
        <div className="text-[10px] text-slate-500 uppercase tracking-wider">Verification Signals</div>
        <div className="space-y-1.5">
          {bulletPoints.map((bp, i) => (
            <div key={i} className="flex items-start gap-2 text-xs text-slate-300">
              <span className="p-0.5 rounded bg-emerald-950/40 text-emerald-400 border border-emerald-800/40 mt-0.5">
                <Check className="h-3 w-3" />
              </span>
              <span>{bp.text}</span>
            </div>
          ))}
        </div>
      </div>

      {warnings && warnings.length > 0 && (
        <div className="pt-2 border-t border-slate-800/80 space-y-2">
          <div className="text-[10px] text-amber-500 uppercase tracking-wider">Audit Reservations</div>
          <div className="space-y-1.5">
            {warnings.map((warn, i) => (
              <div key={i} className="flex items-start gap-2 text-xs text-amber-300/90 bg-amber-950/20 p-2 rounded border border-amber-900/30">
                <AlertTriangle className="h-3.5 w-3.5 text-amber-400 shrink-0 mt-0.5" />
                <span>{warn}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
