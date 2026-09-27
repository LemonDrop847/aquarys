"use client";

import { motion } from "motion/react";
import { AlertOctagon, ArrowDownRight, ShieldAlert, Check, HelpCircle, Sparkles, RefreshCw } from "lucide-react";

interface SkepticChallengeViewProps {
  data: {
    initialConfidence: number;
    revisedConfidence: number;
    alternativeHypotheses: string[];
    criticalCounterEvidence: string[];
    remainingUncertainties: string[];
  };
  onReset?: () => void;
}

export function SkepticChallengeView({ data, onReset }: SkepticChallengeViewProps) {
  const delta = data.initialConfidence - data.revisedConfidence;

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.98 }}
      animate={{ opacity: 1, scale: 1 }}
      className="p-6 rounded-2xl bg-amber-950/20 border border-amber-500/40 space-y-6 font-mono text-xs shadow-2xl"
    >
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-amber-500/20 pb-4">
        <div className="flex items-center gap-2.5 text-amber-400">
          <ShieldAlert className="h-5 w-5 shrink-0" />
          <div>
            <h3 className="text-sm font-bold uppercase tracking-wider text-amber-300">
              ADVERSARIAL SKEPTIC ENGINE ACTIVATED
            </h3>
            <p className="text-[10px] text-amber-400/80">
              Adversarial counter-evaluation applied to prevent confirmation bias and overconfidence.
            </p>
          </div>
        </div>

        {onReset && (
          <button
            onClick={onReset}
            className="px-3 py-1.5 rounded bg-slate-900 border border-slate-700 text-slate-300 hover:text-white text-[10px] uppercase font-bold flex items-center gap-1.5 self-start sm:self-auto"
          >
            <RefreshCw className="h-3 w-3" />
            <span>RESET SKEPTIC CHALLENGE</span>
          </button>
        )}
      </div>

      {/* Uncertainty & Confidence Impact Bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-4 rounded-xl bg-slate-950/80 border border-amber-500/20">
        <div>
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">
            INITIAL ORACLE CONFIDENCE
          </div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">
            {data.initialConfidence}%
          </div>
        </div>

        <div>
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">
            REVISED SKEPTIC CONFIDENCE
          </div>
          <div className="text-2xl font-bold text-amber-400 mt-1 flex items-center gap-2">
            <span>{data.revisedConfidence}%</span>
            <span className="text-xs px-2 py-0.5 rounded bg-amber-950/80 border border-amber-800 text-amber-300">
              -{delta}% PENALTY
            </span>
          </div>
        </div>

        <div>
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">
            UNCERTAINTY STATUS
          </div>
          <div className="text-xs font-bold text-amber-300 mt-2 uppercase">
            EVIDENTIARY DIVERGENCE IDENTIFIED
          </div>
        </div>
      </div>

      {/* Alternative Hypotheses */}
      <div className="space-y-3">
        <div className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <HelpCircle className="h-4 w-4 text-amber-400" />
          <span>PLAUSIBLE ALTERNATIVE EXPLANATIONS</span>
        </div>
        <div className="space-y-2">
          {data.alternativeHypotheses.map((alt, idx) => (
            <div
              key={idx}
              className="p-3 rounded-lg bg-slate-900/60 border border-slate-800/80 text-slate-300 text-xs flex items-start gap-2.5"
            >
              <span className="text-amber-400 font-bold shrink-0">H-ALT-{idx + 1}:</span>
              <p className="leading-relaxed">{alt}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Critical Counter-Evidence */}
      <div className="space-y-3">
        <div className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <AlertOctagon className="h-4 w-4 text-red-400" />
          <span>CRITICAL COUNTER-EVIDENCE VECTORS</span>
        </div>
        <div className="space-y-2">
          {data.criticalCounterEvidence.map((ce, idx) => (
            <div
              key={idx}
              className="p-3 rounded-lg bg-red-950/20 border border-red-900/40 text-red-300 text-xs flex items-start gap-2.5"
            >
              <span className="text-red-400 font-bold shrink-0">CE-{idx + 1}:</span>
              <p className="leading-relaxed">{ce}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Remaining Uncertainties */}
      <div className="space-y-3">
        <div className="text-xs font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <HelpCircle className="h-4 w-4 text-cyan-400" />
          <span>REMAINING SENSITIVITIES & UNCONSTRAINED VARIABLES</span>
        </div>
        <div className="space-y-2">
          {data.remainingUncertainties.map((unc, idx) => (
            <div
              key={idx}
              className="p-3 rounded-lg bg-slate-900/40 border border-slate-800 text-slate-300 text-xs flex items-start gap-2.5"
            >
              <span className="text-cyan-400 font-bold shrink-0">UNC-{idx + 1}:</span>
              <p className="leading-relaxed">{unc}</p>
            </div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
