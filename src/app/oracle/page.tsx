"use client";

import { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { OracleActivityFeed } from "@/components/oracle/OracleActivityFeed";
import { OracleFindingsView } from "@/components/oracle/OracleFindingsView";
import { MOCK_ORACLE_INVESTIGATION } from "@/lib/mock-data";
import { Sparkles, Target, AlertOctagon, HelpCircle } from "lucide-react";
import { motion } from "motion/react";

function OracleContent() {
  const searchParams = useSearchParams();
  const siteId = searchParams.get("siteId") || "site-c1";

  const [isInvestigating, setIsInvestigating] = useState(false);
  const [hasInvestigated, setHasInvestigated] = useState(false);
  const [skepticMode, setSkepticMode] = useState(false);

  const handleInvestigate = () => {
    setIsInvestigating(true);
    setHasInvestigated(false);
  };

  const handleInvestigationComplete = () => {
    setIsInvestigating(false);
    setHasInvestigated(true);
  };

  const handleChallenge = () => {
    setSkepticMode(true);
  };

  const handleResetSkeptic = () => {
    setSkepticMode(false);
  };

  return (
    <div className="space-y-8 font-mono pb-16">
      {/* Page Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-cyan-400 font-bold uppercase tracking-wider text-xs mb-2">
          <Sparkles className="h-4 w-4" />
          <span>AQUARYS ENVIRONMENTAL INTELLIGENCE ORACLE</span>
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-white uppercase">
          Investigation Console
        </h1>
      </div>

      {/* Input Console */}
      <div className="p-6 rounded-2xl bg-slate-950/90 border border-cyan-500/30 shadow-2xl">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-end">
          <div className="space-y-2">
            <label className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Target Stream</label>
            <div className="bg-slate-900 border border-slate-700 px-4 py-3 rounded text-slate-200 font-bold">
              C1 · Coimbra, Rio Mondego
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-[10px] font-bold uppercase tracking-wider text-slate-500">Query</label>
            <div className="bg-slate-900 border border-slate-700 px-4 py-3 rounded text-slate-300">
              What can this stream learn from comparable streams?
            </div>
          </div>
        </div>

        {!hasInvestigated && !isInvestigating && (
          <button
            onClick={handleInvestigate}
            className="mt-6 px-6 py-3 rounded bg-cyan-500 text-slate-950 font-bold uppercase tracking-wider hover:bg-cyan-400 transition-colors flex items-center gap-2"
          >
            <Target className="h-4 w-4" />
            <span>INVESTIGATE EMPIRICAL TRAJECTORIES</span>
          </button>
        )}
      </div>

      {/* Investigation Feed */}
      {isInvestigating && (
        <OracleActivityFeed
          activities={MOCK_ORACLE_INVESTIGATION.activity}
          isInvestigating={isInvestigating}
          onComplete={handleInvestigationComplete}
        />
      )}

      {/* Findings */}
      {hasInvestigated && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <OracleFindingsView
            finding={{
              id: MOCK_ORACLE_INVESTIGATION.id,
              synthesis: MOCK_ORACLE_INVESTIGATION.findings,
              confidence: 88,
              supportingTwins: ["G7"],
              evidenceCitations: [
                { id: "e1", title: "HM Protocol #HM-2026-04", source: "OAH", confidence: 94 },
                { id: "e2", title: "Flemish Agency Dataset", source: "Flemish EA", confidence: 96 }
              ],
              hypotheses: MOCK_ORACLE_INVESTIGATION.hypotheses.map(h => ({
                id: h.id,
                title: h.statement.split('.')[0],
                description: h.statement,
                confidence: h.confidence,
                supportingEvidenceCount: h.supportingEvidence.length
              })),
              counterEvidence: MOCK_ORACLE_INVESTIGATION.counterEvidence.map(c => ({
                description: c,
                severity: "medium"
              })),
              knowledgeGaps: MOCK_ORACLE_INVESTIGATION.dataGaps.map(g => ({
                dimension: g.id,
                impact: "high",
                description: g.description
              })),
              nextObservations: MOCK_ORACLE_INVESTIGATION.nextObservations.map(n => ({
                location: n.location,
                expectedGain: n.expectedInformationGain * 100,
                targetMetric: n.description,
                rationale: "Optimizes basin-wide model.",
                protocol: "Automated sonde deployment."
              }))
            }}
            onChallenge={handleChallenge}
            skepticData={skepticMode ? {
              initialConfidence: 88,
              revisedConfidence: 74,
              alternativeHypotheses: ["Drought impact", "Sampling bias"],
              criticalCounterEvidence: ["Urban culvert runoff", "Channel depth limitations"],
              remainingUncertainties: ["Nutrient loading independence"]
            } : null}
            onResetSkeptic={handleResetSkeptic}
          />
        </motion.div>
      )}
    </div>
  );
}

export default function OraclePage() {
  return (
    <Suspense
      fallback={
        <div className="p-12 text-center font-mono text-xs text-slate-500">
          INITIALIZING ORACLE INTELLIGENCE ENGINE...
        </div>
      }
    >
      <OracleContent />
    </Suspense>
  );
}
