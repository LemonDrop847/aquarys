"use client";

import { useEffect, useState } from "react";
import { OracleActivity } from "@/lib/types";
import { CheckCircle2, Clock, Cpu, Sparkles, Terminal } from "lucide-react";
import { motion } from "motion/react";

interface OracleActivityFeedProps {
  activities: OracleActivity[];
  isInvestigating: boolean;
  onComplete?: () => void;
}

export function OracleActivityFeed({
  activities,
  isInvestigating,
  onComplete
}: OracleActivityFeedProps) {
  const [visibleIndex, setVisibleIndex] = useState(0);

  useEffect(() => {
    if (!isInvestigating) {
      setVisibleIndex(activities.length);
      return;
    }

    setVisibleIndex(1);
    const interval = setInterval(() => {
      setVisibleIndex((prev) => {
        if (prev < activities.length) {
          return prev + 1;
        } else {
          clearInterval(interval);
          if (onComplete) {
            setTimeout(onComplete, 400);
          }
          return prev;
        }
      });
    }, 400);

    return () => clearInterval(interval);
  }, [isInvestigating, activities.length, onComplete]);

  return (
    <div className="rounded-xl bg-slate-950/90 border border-cyan-500/30 p-5 font-mono text-xs space-y-4 shadow-2xl">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-2 text-cyan-400">
          <Terminal className="h-4 w-4 animate-pulse" />
          <span className="font-bold uppercase tracking-wider">
            ORACLE MULTI-STEP REASONING STREAM
          </span>
        </div>
        <div className="flex items-center gap-2 text-[10px] text-slate-500">
          <Clock className="h-3 w-3" />
          <span>{isInvestigating ? "EVALUATING CROSS-BASIN EVIDENCE..." : "COMPLETED 9/9 STEPS"}</span>
        </div>
      </div>

      <div className="space-y-2">
        {activities.map((act, index) => {
          const isDone = index < visibleIndex;
          const isCurrent = index === visibleIndex - 1 && isInvestigating;

          return (
            <motion.div
              key={act.step}
              initial={{ opacity: 0, x: -10 }}
              animate={{
                opacity: isDone ? 1 : 0.25,
                x: isDone ? 0 : -5
              }}
              transition={{ duration: 0.2 }}
              className={`flex items-center justify-between p-2.5 rounded transition-colors ${
                isCurrent
                  ? "bg-cyan-950/40 text-cyan-300 border border-cyan-800/40"
                  : isDone
                  ? "bg-slate-900/40 text-slate-300 border border-slate-800/60"
                  : "text-slate-600 border border-transparent"
              }`}
            >
              <div className="flex items-center gap-2.5">
                {isDone && !isCurrent ? (
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400 shrink-0" />
                ) : isCurrent ? (
                  <div className="h-2 w-2 rounded-full bg-cyan-400 animate-ping shrink-0" />
                ) : (
                  <div className="h-2 w-2 rounded-full bg-slate-700 shrink-0" />
                )}
                <span className="text-[11px] font-medium">{act.label}</span>
              </div>
              <span className="text-[10px] text-slate-500">{act.timestamp}</span>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
}
