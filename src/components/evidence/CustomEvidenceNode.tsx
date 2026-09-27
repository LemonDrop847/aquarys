"use client";

import { memo } from "react";
import { Handle, Position, NodeProps, Node } from "@xyflow/react";
import { EvidenceNode } from "@/lib/types";

const NODE_COLORS = {
  claim: { bg: "bg-cyan-950/80", border: "border-cyan-500/50", text: "text-cyan-300" },
  observation: { bg: "bg-emerald-950/80", border: "border-emerald-500/50", text: "text-emerald-300" },
  measurement: { bg: "bg-blue-950/80", border: "border-blue-500/50", text: "text-blue-300" },
  eo_signal: { bg: "bg-purple-950/80", border: "border-purple-500/50", text: "text-purple-300" },
  site: { bg: "bg-amber-950/80", border: "border-amber-500/50", text: "text-amber-300" },
  hypothesis: { bg: "bg-rose-950/80", border: "border-rose-500/50", text: "text-rose-300" },
  intervention: { bg: "bg-indigo-950/80", border: "border-indigo-500/50", text: "text-indigo-300" }
};

export type EvidenceCustomNodeType = Node<{ type: string; label: string; description?: string; confidence?: number } & Record<string, unknown>>;

export const CustomEvidenceNode = memo(({ data, selected }: NodeProps<EvidenceCustomNodeType>) => {
  const nodeData = (data || {}) as EvidenceCustomNodeType["data"];
  const colors = (nodeData.type && NODE_COLORS[nodeData.type as keyof typeof NODE_COLORS]) || NODE_COLORS.claim;

  return (
    <div
      className={`px-4 py-3 rounded-lg border-2 ${colors.bg} ${colors.border} ${
        selected ? "ring-2 ring-cyan-400/50" : ""
      } min-w-[180px] max-w-[280px] font-mono text-xs shadow-lg transition-all`}
    >
      <Handle type="target" position={Position.Top} className="w-2 h-2 bg-slate-400" />

      <div className="space-y-1.5">
        <div className={`text-[10px] uppercase font-bold ${colors.text} tracking-wider`}>
          {nodeData.type ? nodeData.type.replace("_", " ") : "NODE"}
        </div>

        <div className="text-slate-100 font-semibold leading-tight">
          {nodeData.label || "Unnamed"}
        </div>

        {nodeData.description && (
          <div className="text-[11px] text-slate-400 leading-relaxed">
            {nodeData.description}
          </div>
        )}

        {nodeData.confidence !== undefined && (
          <div className="pt-1 flex items-center gap-1.5 text-[10px] text-slate-500">
            <span>CONFIDENCE:</span>
            <span className="text-emerald-400 font-bold">{nodeData.confidence}%</span>
          </div>
        )}
      </div>

      <Handle type="source" position={Position.Bottom} className="w-2 h-2 bg-slate-400" />
    </div>
  );
});

CustomEvidenceNode.displayName = "CustomEvidenceNode";
