"use client";

import { TwinMatch } from "@/lib/types";
import { GitCompare, AlertTriangle, ArrowRight, TrendingUp, ShieldCheck, Check, Info } from "lucide-react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from "recharts";
import { motion } from "motion/react";

interface TwinComparisonViewProps {
  comparison: {
    siteA: { code: string; name: string; country: string; basin: string };
    siteB: { code: string; name: string; country: string; basin: string };
    differentialMetrics: {
      metric: string;
      valueA: string | number;
      valueB: string | number;
      impact: "positive" | "warning" | "neutral";
    }[];
    differentiators: {
      title: string;
      description: string;
    }[];
    timeline: { timestamp: string; siteAValue: number; siteBValue: number }[];
  };
}

export function TwinComparisonView({ comparison }: TwinComparisonViewProps) {
  const { siteA, siteB, differentialMetrics, differentiators, timeline } = comparison;

  return (
    <div className="space-y-8 font-mono">
      {/* Split Header */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Site A (Your Stream) */}
        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] px-2 py-0.5 rounded bg-cyan-950/80 text-cyan-400 font-bold border border-cyan-800/60">
              YOUR TARGET STREAM
            </span>
            <span className="text-xs text-slate-400 uppercase">{siteA.country}</span>
          </div>
          <div className="text-2xl font-bold text-slate-100 uppercase tracking-tight">
            {siteA.code} · {siteA.name}
          </div>
          <p className="text-xs text-slate-400">
            {siteA.basin} Basin · Urban Hydrology Focus
          </p>
        </div>

        {/* Site B (Twin) */}
        <div className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950/80 text-emerald-400 font-bold border border-emerald-800/60">
              DISCOVERED ECOLOGICAL TWIN
            </span>
            <span className="text-xs text-slate-400 uppercase">{siteB.country}</span>
          </div>
          <div className="text-2xl font-bold text-slate-100 uppercase tracking-tight">
            {siteB.code} · {siteB.name}
          </div>
          <p className="text-xs text-slate-400">
            {siteB.basin} Basin · 92% Trajectory Correlation
          </p>
        </div>
      </div>

      {/* Synchronized Trajectory Timelines */}
      <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <span className="text-[10px] text-cyan-400 uppercase tracking-wider block">
              SYNCHRONIZED TIMELINE RECONSTRUCTION
            </span>
            <h3 className="text-sm font-bold text-slate-200 uppercase">
              Longitudinal Ecosystem Trajectory Comparison
            </h3>
          </div>
          <div className="flex items-center gap-4 text-xs">
            <div className="flex items-center gap-1.5 text-cyan-400">
              <span className="h-2 w-2 rounded-full bg-cyan-400" />
              <span>{siteA.code} ({siteA.name})</span>
            </div>
            <div className="flex items-center gap-1.5 text-emerald-400">
              <span className="h-2 w-2 rounded-full bg-emerald-400" />
              <span>{siteB.code} ({siteB.name})</span>
            </div>
          </div>
        </div>

        <div className="h-64 w-full pt-4">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={timeline} margin={{ top: 5, right: 20, bottom: 5, left: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="timestamp" stroke="#64748b" tick={{ fontSize: 10 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#020617",
                  borderColor: "#334155",
                  borderRadius: "8px",
                  fontSize: "11px",
                  fontFamily: "monospace"
                }}
              />
              <Line
                type="monotone"
                dataKey="siteAValue"
                name={`${siteA.code} (Your Stream)`}
                stroke="#22d3ee"
                strokeWidth={2}
                dot={{ r: 3, fill: "#22d3ee" }}
              />
              <Line
                type="monotone"
                dataKey="siteBValue"
                name={`${siteB.code} (Twin)`}
                stroke="#34d399"
                strokeWidth={2}
                dot={{ r: 3, fill: "#34d399" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Differential Metrics Comparison Matrix */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <span className="text-[10px] text-slate-400 uppercase tracking-wider">
            DIFFERENTIAL METRIC MATRIX
          </span>
          <span className="text-[10px] text-slate-500">DELTA TOLERANCE ±5%</span>
        </div>

        <div className="rounded-xl bg-slate-900/60 border border-slate-800 overflow-hidden divide-y divide-slate-800">
          <div className="grid grid-cols-12 p-3 bg-slate-950/80 text-[10px] uppercase text-slate-500 font-bold">
            <div className="col-span-4">Metric Dimension</div>
            <div className="col-span-3 text-center">{siteA.code} ({siteA.name})</div>
            <div className="col-span-3 text-center">{siteB.code} ({siteB.name})</div>
            <div className="col-span-2 text-right">Variance / Status</div>
          </div>

          {differentialMetrics.map((m, idx) => (
            <div
              key={idx}
              className="grid grid-cols-12 p-3.5 items-center text-xs hover:bg-slate-800/30 transition-colors"
            >
              <div className="col-span-4 font-semibold text-slate-200 uppercase">
                {m.metric}
              </div>
              <div className="col-span-3 text-center font-bold text-cyan-400">
                {m.valueA}
              </div>
              <div className="col-span-3 text-center font-bold text-emerald-400">
                {m.valueB}
              </div>
              <div className="col-span-2 text-right">
                <span
                  className={`text-[10px] px-2 py-0.5 rounded font-bold inline-block uppercase ${
                    m.impact === "positive"
                      ? "bg-emerald-950/60 text-emerald-400 border border-emerald-800/50"
                      : m.impact === "warning"
                      ? "bg-amber-950/60 text-amber-400 border border-amber-800/50"
                      : "bg-slate-800 text-slate-300"
                  }`}
                >
                  {m.impact === "positive" ? "ALIGNED" : m.impact === "warning" ? "DIVERGENT" : "NEUTRAL"}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Potential Differentiators & Mandatory Disclaimer */}
      <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4 text-cyan-400" />
            <h3 className="text-xs uppercase font-bold text-slate-100 tracking-wider">
              POTENTIAL DIFFERENTIATORS
            </h3>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {differentiators.map((diff, i) => (
            <div
              key={i}
              className="p-4 rounded-lg bg-slate-950/70 border border-slate-800/90 space-y-2"
            >
              <div className="text-xs font-bold text-cyan-300 uppercase flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-400" />
                {diff.title}
              </div>
              <p className="text-xs text-slate-400 leading-relaxed">
                {diff.description}
              </p>
            </div>
          ))}
        </div>

        {/* Mandatory Scientific Disclaimer Banner */}
        <div className="p-4 rounded-lg bg-amber-950/20 border border-amber-500/30 text-xs flex items-start gap-3 mt-4">
          <AlertTriangle className="h-4 w-4 text-amber-400 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <div className="font-bold text-amber-300 uppercase tracking-wide text-[11px]">
              SCIENTIFIC VALIDATION DISCLAIMER
            </div>
            <p className="text-amber-400/80 leading-relaxed text-[11px]">
              These are associated factors and comparative vector correlations, not causal conclusions. Field verification and controlled chemical/biological sampling are required prior to remediation decisions.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}