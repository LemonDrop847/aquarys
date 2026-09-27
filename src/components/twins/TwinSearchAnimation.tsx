"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { Search, Globe2, Cpu, CheckCircle2, Waves, Network } from "lucide-react";

interface TwinSearchAnimationProps {
  isSearching: boolean;
  onSearchComplete?: () => void;
  siteName: string;
}

const SEARCH_STAGES = [
  { label: "INITIALIZING EUROPEAN HYDRO-VECTOR EMBEDDING MATRIX", progress: 15 },
  { label: "QUERYING OAH SENSOR NETWORK & SENTINEL-2 BASIN TOPOLOGIES", progress: 38 },
  { label: "COMPUTING MULTI-DIMENSIONAL STREAM FINGERPRINT DISTANCES", progress: 65 },
  { label: "FILTERING TEMPORALLY SYNCHRONIZED TRAJECTORIES", progress: 85 },
  { label: "FINALIZING HIGH-CONFIDENCE ECOLOGICAL TWIN CLUSTERS", progress: 100 }
];

export function TwinSearchAnimation({
  isSearching,
  onSearchComplete,
  siteName
}: TwinSearchAnimationProps) {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (!isSearching) {
      setCurrentStep(0);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStep((prev) => {
        if (prev < SEARCH_STAGES.length - 1) {
          return prev + 1;
        } else {
          clearInterval(interval);
          if (onSearchComplete) {
            setTimeout(onSearchComplete, 600);
          }
          return prev;
        }
      });
    }, 450);

    return () => clearInterval(interval);
  }, [isSearching, onSearchComplete]);

  if (!isSearching) return null;

  const currentStage = SEARCH_STAGES[currentStep];

  return (
    <div className="w-full max-w-2xl mx-auto p-8 rounded-2xl bg-slate-900/90 border border-cyan-500/30 shadow-2xl font-mono text-xs">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4 mb-6">
        <div className="flex items-center gap-2.5 text-cyan-400">
          <Network className="h-4 w-4 animate-pulse" />
          <span className="font-bold uppercase tracking-wider">
            ECOLOGICAL TWIN DISCOVERY ENGINE
          </span>
        </div>
        <span className="text-[10px] text-slate-500 uppercase tracking-widest">
          VECTOR SEARCH RUNNING
        </span>
      </div>

      <div className="space-y-6">
        {/* Animated radar visualizer */}
        <div className="relative h-32 w-full rounded-xl bg-slate-950/80 border border-slate-800 flex items-center justify-center overflow-hidden">
          {/* Concentric radar rings */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-48 h-48 rounded-full border border-cyan-500/20 animate-ping duration-1000" />
            <div className="w-32 h-32 rounded-full border border-emerald-500/20" />
            <div className="w-16 h-16 rounded-full border border-cyan-400/40" />
          </div>

          {/* Scanner sweep line */}
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
            className="absolute inset-0 flex items-center justify-center"
          >
            <div className="w-1/2 h-0.5 bg-gradient-to-r from-transparent to-cyan-400 origin-left" />
          </motion.div>

          <div className="relative z-10 text-center space-y-1">
            <div className="text-slate-200 font-bold uppercase tracking-wide">
              FINDING ECOLOGICAL TWINS FOR {siteName}
            </div>
            <div className="text-[10px] text-slate-400">
              SCANNING 2,410 BASINS ACROSS EUROPE
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-[11px] text-slate-400">
            <span>{currentStage.label}</span>
            <span className="text-cyan-400 font-bold">{currentStage.progress}%</span>
          </div>
          <div className="h-1.5 w-full bg-slate-950 rounded-full overflow-hidden border border-slate-800">
            <motion.div
              className="h-full bg-gradient-to-r from-cyan-500 to-emerald-400"
              initial={{ width: "0%" }}
              animate={{ width: `${currentStage.progress}%` }}
              transition={{ ease: "easeInOut", duration: 0.3 }}
            />
          </div>
        </div>

        {/* Stage List */}
        <div className="space-y-1.5 pt-2">
          {SEARCH_STAGES.map((stage, idx) => {
            const isCompleted = idx < currentStep;
            const isCurrent = idx === currentStep;

            return (
              <div
                key={idx}
                className={`flex items-center justify-between px-3 py-1.5 rounded transition-colors text-[10px] ${
                  isCurrent
                    ? "bg-cyan-950/40 text-cyan-300 border border-cyan-800/40"
                    : isCompleted
                    ? "text-slate-400"
                    : "text-slate-600"
                }`}
              >
                <div className="flex items-center gap-2">
                  {isCompleted ? (
                    <CheckCircle2 className="h-3 w-3 text-emerald-400 shrink-0" />
                  ) : isCurrent ? (
                    <div className="h-2 w-2 rounded-full bg-cyan-400 animate-ping shrink-0" />
                  ) : (
                    <div className="h-2 w-2 rounded-full bg-slate-700 shrink-0" />
                  )}
                  <span className="truncate">{stage.label}</span>
                </div>
                <span>{isCompleted ? "DONE" : isCurrent ? "COMPUTING" : "WAITING"}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
