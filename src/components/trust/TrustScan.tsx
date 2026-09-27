"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { CheckCircle2, ShieldCheck, Terminal, Cpu } from "lucide-react";

interface TrustScanProps {
  onScanComplete?: () => void;
  scanning: boolean;
}

const SCAN_STEPS = [
  { id: "schema", label: "Schema Validation & Typology Verification" },
  { id: "completeness", label: "Attribute Completeness & Null Audit" },
  { id: "location", label: "Geospatial Alignment & Precision Check" },
  { id: "temporal", label: "Temporal Validity & Ephemeral Drift" },
  { id: "duplicates", label: "Duplicate & Spurious Signal Detection" },
  { id: "corroboration", label: "Independent Observer & Satellite Corroboration" }
];

export function TrustScan({ onScanComplete, scanning }: TrustScanProps) {
  const [completedSteps, setCompletedSteps] = useState<string[]>([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  useEffect(() => {
    if (!scanning) {
      setCompletedSteps(SCAN_STEPS.map((s) => s.id));
      return;
    }

    setCompletedSteps([]);
    setCurrentStepIndex(0);

    const interval = setInterval(() => {
      setCurrentStepIndex((prev) => {
        if (prev < SCAN_STEPS.length) {
          setCompletedSteps((curr) => [...curr, SCAN_STEPS[prev].id]);
          return prev + 1;
        } else {
          clearInterval(interval);
          if (onScanComplete) onScanComplete();
          return prev;
        }
      });
    }, 280);

    return () => clearInterval(interval);
  }, [scanning, onScanComplete]);

  return (
    <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 font-mono">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 text-xs text-slate-300">
        <div className="flex items-center gap-2">
          <Cpu className="h-4 w-4 text-cyan-400" />
          <span className="font-semibold uppercase tracking-wider text-cyan-400">
            EVIDENCE INTEGRITY AUDIT MATRIX
          </span>
        </div>
        <div className="text-[10px] text-slate-500 flex items-center gap-1.5">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
          {completedSteps.length === SCAN_STEPS.length ? "AUDIT VERIFIED" : "AUDIT IN PROGRESS"}
        </div>
      </div>

      <div className="mt-4 space-y-2.5">
        {SCAN_STEPS.map((step, idx) => {
          const isDone = completedSteps.includes(step.id);
          const isCurrent = currentStepIndex === idx && scanning;

          return (
            <div
              key={step.id}
              className={`flex items-center justify-between text-xs px-3 py-2 rounded border transition-all ${
                isDone
                  ? "bg-slate-950/60 border-slate-800/80 text-slate-200"
                  : isCurrent
                  ? "bg-cyan-950/20 border-cyan-800/50 text-cyan-200"
                  : "bg-slate-950/20 border-slate-900 text-slate-600"
              }`}
            >
              <div className="flex items-center gap-2.5">
                <span className="text-[10px] text-slate-500 font-mono">0{idx + 1}</span>
                <span>{step.label}</span>
              </div>
              <div>
                {isDone ? (
                  <motion.div
                    initial={{ scale: 0.8, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="flex items-center gap-1 text-emerald-400 text-[11px]"
                  >
                    <CheckCircle2 className="h-3.5 w-3.5" />
                    <span>PASSED</span>
                  </motion.div>
                ) : isCurrent ? (
                  <span className="text-cyan-400 text-[11px] animate-pulse">ANALYZING...</span>
                ) : (
                  <span className="text-slate-700 text-[11px]">QUEUED</span>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
