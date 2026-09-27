"use client";

import { useState } from "react";
import { OracleFinding, OracleHypothesis, OracleGap, NextObservation } from "@/lib/types";
import {
  AlertOctagon,
  ArrowRight,
  CheckCircle2,
  ExternalLink,
  HelpCircle,
  Layers,
  Lightbulb,
  ShieldAlert,
  Sparkles,
  Target,
  TrendingUp,
  FileDown
} from "lucide-react";
import { motion } from "motion/react";
import Link from "next/link";
import { SkepticChallengeView } from "./SkepticChallengeView";

interface OracleFindingsViewProps {
  finding: OracleFinding;
  onChallenge?: () => void;
  skepticData?: {
    initialConfidence: number;
    revisedConfidence: number;
    alternativeHypotheses: string[];
    criticalCounterEvidence: string[];
    remainingUncertainties: string[];
  } | null;
  onResetSkeptic?: () => void;
}

export function OracleFindingsView({
  finding,
  onChallenge,
  skepticData,
  onResetSkeptic
}: OracleFindingsViewProps) {
  return (
    <div className="space-y-8 font-mono">
      {/* Primary Finding Card */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-5 shadow-2xl relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
          <div className="flex items-center gap-2 text-cyan-400">
            <Sparkles className="h-4 w-4" />
            <span className="text-xs font-bold uppercase tracking-wider">
              SYNTHESIZED CROSS-BASIN FINDING
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider">
              CONFIDENCE RATING:
            </span>
            <span className="text-sm font-bold text-emerald-400 px-2.5 py-0.5 rounded bg-emerald-950/80 border border-emerald-800/60">
              {finding.confidence}%
            </span>
          </div>
        </div>

        {/* Synthesis Text */}
        <div className="space-y-2">
          <h2 className="text-lg font-bold text-slate-100 tracking-tight leading-snug">
            {finding.synthesis}
          </h2>
          <p className="text-xs text-slate-400 leading-relaxed max-w-4xl">
            Synthesized across 3 hydromorphic twin trajectories ({finding.supportingTwins.join(", ")}) and verified against 14 corroborating biological and physicochemical observations.
          </p>
        </div>

        {/* Supporting Evidence Citations */}
        <div className="space-y-2 pt-2 border-t border-slate-800/60">
          <div className="text-[10px] text-slate-500 uppercase tracking-wider">
            CORROBORATING EVIDENCE CITATIONS (CLICK TO PROVE PROVENANCE):
          </div>
          <div className="flex flex-wrap gap-2">
            {finding.evidenceCitations.map((cit) => (
              <Link
                key={cit.id}
                href={`/evidence/${cit.id}`}
                className="group px-3 py-1.5 rounded-lg bg-slate-950/80 border border-slate-800 hover:border-cyan-500/60 transition-all flex items-center gap-2 text-xs"
              >
                <span className="text-cyan-400 font-bold group-hover:underline">
                  [{cit.id}]
                </span>
                <span className="text-slate-300">{cit.title}</span>
                <span className="text-[10px] text-slate-500 uppercase">
                  ({cit.source} · {cit.confidence}%)
                </span>
                <ExternalLink className="h-3 w-3 text-slate-600 group-hover:text-cyan-400 ml-0.5" />
              </Link>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Skeptic Challenge Section (If Activated) */}
      {skepticData ? (
        <SkepticChallengeView data={skepticData} onReset={onResetSkeptic} />
      ) : (
        <div className="p-4 rounded-xl bg-amber-950/10 border border-amber-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3 text-amber-400">
            <ShieldAlert className="h-5 w-5 shrink-0" />
            <div>
              <div className="text-xs font-bold uppercase tracking-wider text-amber-300">
                WANT TO TEST FOR CONFIRMATION BIAS?
              </div>
              <p className="text-[11px] text-amber-400/80">
                Run the Adversarial Skeptic to discover counter-evidence, alternative causal explanations, and revise confidence.
              </p>
            </div>
          </div>
          <button
            onClick={onChallenge}
            className="px-4 py-2 rounded bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/50 text-xs font-bold uppercase tracking-wider flex items-center gap-2 shrink-0 transition-colors"
          >
            <ShieldAlert className="h-3.5 w-3.5" />
            <span>CHALLENGE WITH SKEPTIC</span>
          </button>
        </div>
      )}

      {/* Grounded Hypotheses */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-slate-200 text-xs font-bold uppercase tracking-wider">
            <Lightbulb className="h-4 w-4 text-cyan-400" />
            <span>GROUNDED ECOLOGICAL HYPOTHESES</span>
          </div>
          <div className="text-[10px] text-slate-500">
            RANKED BY EMPIRICAL TRAJECTORY FIT
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {finding.hypotheses.map((hypo) => (
            <div
              key={hypo.id}
              className="p-5 rounded-xl bg-slate-900/50 border border-slate-800 space-y-3"
            >
              <div className="flex items-start justify-between gap-3">
                <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 font-bold border border-cyan-800/60">
                  {hypo.id}
                </span>
                <span className="text-xs font-bold text-cyan-400">
                  {hypo.confidence}% FIT
                </span>
              </div>

              <h4 className="text-sm font-bold text-slate-100 uppercase">
                {hypo.title}
              </h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                {hypo.description}
              </p>

              <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-slate-500">
                <span>SUPPORTED BY: {hypo.supportingEvidenceCount} OBSERVATIONS</span>
                <span className="text-emerald-400 font-bold">VERIFIED</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Critical Counter-Evidence & Data Gaps Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Counter-Evidence */}
        <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800 space-y-4">
          <div className="flex items-center gap-2 text-red-400 text-xs font-bold uppercase tracking-wider border-b border-slate-800 pb-3">
            <AlertOctagon className="h-4 w-4" />
            <span>DETECTED COUNTER-EVIDENCE</span>
          </div>

          <div className="space-y-3">
            {finding.counterEvidence.map((ce, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-lg bg-red-950/10 border border-red-900/30 text-xs text-red-300 space-y-1"
              >
                <div className="flex items-center justify-between font-bold text-[11px]">
                  <span>VULNERABILITY #{idx + 1}</span>
                  <span className="text-[10px] uppercase text-red-400/80">
                    SEVERITY: {ce.severity.toUpperCase()}
                  </span>
                </div>
                <p className="text-slate-300 text-[11px] leading-relaxed">
                  {ce.description}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Data Gaps */}
        <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800 space-y-4">
          <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider border-b border-slate-800 pb-3">
            <HelpCircle className="h-4 w-4" />
            <span>CRITICAL KNOWLEDGE GAPS</span>
          </div>

          <div className="space-y-3">
            {finding.knowledgeGaps.map((gap, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-lg bg-slate-950/80 border border-slate-800 text-xs space-y-1"
              >
                <div className="flex items-center justify-between font-bold text-[11px] text-amber-400">
                  <span>{gap.dimension.toUpperCase()} UNCERTAINTY</span>
                  <span className="text-[10px] text-slate-500">
                    IMPACT: {gap.impact.toUpperCase()}
                  </span>
                </div>
                <p className="text-slate-300 text-[11px] leading-relaxed">
                  {gap.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Next Best Observations (Targeted Missions) */}
      <div className="p-6 rounded-2xl bg-cyan-950/20 border border-cyan-500/30 space-y-5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-cyan-500/20 pb-4">
          <div className="flex items-center gap-2 text-cyan-400">
            <Target className="h-4 w-4" />
            <span className="text-xs font-bold uppercase tracking-wider">
              RECOMMENDED NEXT BEST OBSERVATIONS (UNCERTAINTY REDUCTION)
            </span>
          </div>
          <Link
            href="/missions"
            className="px-3 py-1.5 rounded bg-cyan-500 text-slate-950 font-bold text-[10px] uppercase tracking-wider hover:bg-cyan-400 transition-colors flex items-center gap-1.5 self-start sm:self-auto"
          >
            <span>CONVERT TO VOLUNTEER MISSION</span>
            <ArrowRight className="h-3 w-3" />
          </Link>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {finding.nextObservations.map((obs, idx) => (
            <div
              key={idx}
              className="p-4 rounded-xl bg-slate-950/90 border border-cyan-500/20 space-y-3 flex flex-col justify-between"
            >
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] text-cyan-400 font-bold uppercase">
                    TARGET: {obs.location}
                  </span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
                    +{obs.expectedGain}% GAIN
                  </span>
                </div>
                <div className="text-xs font-bold text-slate-200">
                  {obs.targetMetric}
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  {obs.rationale}
                </p>
              </div>

              <div className="text-[10px] text-slate-500 pt-2 border-t border-slate-800/80">
                RECOMMENDED PROTOCOL: {obs.protocol}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
