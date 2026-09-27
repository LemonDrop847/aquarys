"use client";

import { use } from "react";
import { useEvidenceGraph } from "@/hooks/use-evidence-graph";
import { EvidenceGraphView } from "@/components/evidence/EvidenceGraphView";
import { Layers, ArrowLeft, AlertCircle } from "lucide-react";
import Link from "next/link";
import { motion } from "motion/react";

export default function EvidencePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const { data: graph, isLoading, error } = useEvidenceGraph(id);

  if (isLoading) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center space-y-3">
          <div className="h-8 w-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-xs text-slate-400 font-mono uppercase tracking-wider">
            Loading evidence graph...
          </p>
        </div>
      </div>
    );
  }

  if (error || !graph) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center">
        <div className="text-center space-y-3 max-w-md">
          <AlertCircle className="h-12 w-12 text-red-400 mx-auto" />
          <p className="text-sm text-slate-300 font-mono">
            Evidence graph not found or could not be loaded.
          </p>
          <Link
            href="/oracle"
            className="inline-block px-4 py-2 rounded bg-slate-800 text-slate-300 hover:bg-slate-700 transition-colors text-xs font-mono uppercase"
          >
            Return to Oracle
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 font-mono pb-16">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <Link
          href="/oracle"
          className="inline-flex items-center gap-2 text-xs text-cyan-400 hover:text-cyan-300 transition-colors mb-4"
        >
          <ArrowLeft className="h-3 w-3" />
          <span>BACK TO ORACLE</span>
        </Link>

        <div className="flex items-center gap-2 text-cyan-400 font-bold uppercase tracking-wider text-xs mb-2">
          <Layers className="h-4 w-4" />
          <span>EVIDENCE PROVENANCE GRAPH</span>
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-white uppercase">
          Multi-Entity Evidence Network
        </h1>
        <p className="text-sm text-slate-400 mt-2">
          Interactive visualization of claim provenance, observation lineage, and cross-entity
          correlations. Click nodes to inspect metadata and source records.
        </p>
      </div>

      {/* Graph Stats */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        <div className="p-4 rounded-lg bg-slate-900/60 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase mb-1">Total Nodes</div>
          <div className="text-2xl font-bold text-slate-100">{graph.nodes.length}</div>
        </div>
        <div className="p-4 rounded-lg bg-slate-900/60 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase mb-1">Relationships</div>
          <div className="text-2xl font-bold text-slate-100">{graph.edges.length}</div>
        </div>
        <div className="p-4 rounded-lg bg-slate-900/60 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase mb-1">Node Types</div>
          <div className="text-2xl font-bold text-slate-100">
            {new Set(graph.nodes.map((n) => n.type)).size}
          </div>
        </div>
        <div className="p-4 rounded-lg bg-slate-900/60 border border-slate-800">
          <div className="text-[10px] text-slate-500 uppercase mb-1">Edge Types</div>
          <div className="text-2xl font-bold text-slate-100">
            {new Set(graph.edges.map((e) => e.type)).size}
          </div>
        </div>
      </motion.div>

      {/* Legend */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="p-5 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4"
      >
        <div className="text-xs font-bold text-slate-200 uppercase tracking-wider">
          Legend
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <div className="text-[10px] text-slate-500 uppercase">Node Types</div>
            <div className="flex flex-wrap gap-2">
              <span className="px-2 py-1 rounded bg-cyan-950/80 border border-cyan-500/50 text-cyan-300 text-[10px] font-bold">
                CLAIM
              </span>
              <span className="px-2 py-1 rounded bg-emerald-950/80 border border-emerald-500/50 text-emerald-300 text-[10px] font-bold">
                OBSERVATION
              </span>
              <span className="px-2 py-1 rounded bg-blue-950/80 border border-blue-500/50 text-blue-300 text-[10px] font-bold">
                MEASUREMENT
              </span>
              <span className="px-2 py-1 rounded bg-purple-950/80 border border-purple-500/50 text-purple-300 text-[10px] font-bold">
                EO SIGNAL
              </span>
              <span className="px-2 py-1 rounded bg-amber-950/80 border border-amber-500/50 text-amber-300 text-[10px] font-bold">
                SITE
              </span>
              <span className="px-2 py-1 rounded bg-rose-950/80 border border-rose-500/50 text-rose-300 text-[10px] font-bold">
                HYPOTHESIS
              </span>
              <span className="px-2 py-1 rounded bg-indigo-950/80 border border-indigo-500/50 text-indigo-300 text-[10px] font-bold">
                INTERVENTION
              </span>
            </div>
          </div>

          <div className="space-y-2">
            <div className="text-[10px] text-slate-500 uppercase">Edge Types</div>
            <div className="space-y-1.5 text-[11px]">
              <div className="flex items-center gap-2">
                <div className="h-0.5 w-6 bg-emerald-500" />
                <span className="text-slate-300">supports</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-0.5 w-6 bg-red-500" />
                <span className="text-slate-300">contradicts</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-0.5 w-6 bg-blue-500" />
                <span className="text-slate-300">derived_from</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-0.5 w-6 bg-purple-500" />
                <span className="text-slate-300">correlates</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="h-0.5 w-6 bg-amber-500" />
                <span className="text-slate-300">located_at</span>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Graph */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <EvidenceGraphView graph={graph} />
      </motion.div>

      {/* Instructions */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="p-4 rounded-lg bg-slate-950/60 border border-slate-800 text-xs text-slate-400 space-y-2"
      >
        <div className="font-bold text-slate-300 uppercase">Graph Controls</div>
        <ul className="space-y-1 list-disc list-inside">
          <li>Click and drag to pan the graph</li>
          <li>Scroll or pinch to zoom</li>
          <li>Click a node to open the inspector panel</li>
          <li>Use minimap (bottom-right) for navigation</li>
          <li>Edge thickness indicates relationship strength</li>
        </ul>
      </motion.div>
    </div>
  );
}
