"use client";

import { EvidenceNode } from "@/lib/types";
import { X, ExternalLink, MapPin, Calendar, Award } from "lucide-react";

interface NodeInspectorProps {
  node: EvidenceNode | null;
  onClose: () => void;
}

export function NodeInspector({ node, onClose }: NodeInspectorProps) {
  if (!node) return null;

  return (
    <div className="absolute top-4 right-4 w-80 bg-slate-900/95 border border-slate-700 rounded-xl shadow-2xl font-mono text-xs z-10 backdrop-blur-sm">
      <div className="flex items-center justify-between p-4 border-b border-slate-800">
        <span className="text-cyan-400 font-bold uppercase tracking-wider">
          NODE INSPECTOR
        </span>
        <button
          onClick={onClose}
          className="p-1 hover:bg-slate-800 rounded transition-colors"
          aria-label="Close inspector"
        >
          <X className="h-4 w-4 text-slate-400" />
        </button>
      </div>

      <div className="p-4 space-y-4">
        <div>
          <div className="text-[10px] text-slate-500 uppercase mb-1">NODE TYPE</div>
          <div className="text-slate-100 font-bold uppercase">
            {node.type.replace("_", " ")}
          </div>
        </div>

        <div>
          <div className="text-[10px] text-slate-500 uppercase mb-1">LABEL</div>
          <div className="text-slate-200 leading-relaxed">{node.label}</div>
        </div>

        {node.description && (
          <div>
            <div className="text-[10px] text-slate-500 uppercase mb-1">DESCRIPTION</div>
            <div className="text-slate-300 text-[11px] leading-relaxed">{node.description}</div>
          </div>
        )}

        {node.source && (
          <div>
            <div className="text-[10px] text-slate-500 uppercase mb-1 flex items-center gap-1.5">
              <MapPin className="h-3 w-3" />
              <span>SOURCE</span>
            </div>
            <div className="text-slate-200 font-semibold">{node.source}</div>
          </div>
        )}

        {node.sourceId && (
          <div>
            <div className="text-[10px] text-slate-500 uppercase mb-1">SOURCE ID</div>
            <div className="text-slate-300 font-mono text-[11px]">{node.sourceId}</div>
          </div>
        )}

        {node.observedAt && (
          <div>
            <div className="text-[10px] text-slate-500 uppercase mb-1 flex items-center gap-1.5">
              <Calendar className="h-3 w-3" />
              <span>OBSERVED</span>
            </div>
            <div className="text-slate-300">
              {new Date(node.observedAt).toLocaleDateString("en-US", {
                year: "numeric",
                month: "short",
                day: "numeric"
              })}
            </div>
          </div>
        )}

        {node.confidence !== undefined && (
          <div>
            <div className="text-[10px] text-slate-500 uppercase mb-1 flex items-center gap-1.5">
              <Award className="h-3 w-3" />
              <span>CONFIDENCE RATING</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-emerald-500 transition-all"
                  style={{ width: `${node.confidence}%` }}
                />
              </div>
              <span className="text-emerald-400 font-bold">{node.confidence}%</span>
            </div>
          </div>
        )}

        {node.sourceId && (
          <button className="w-full mt-4 px-3 py-2 rounded bg-cyan-950/80 border border-cyan-800/60 text-cyan-300 hover:bg-cyan-900/80 transition-colors flex items-center justify-center gap-2 text-[11px] font-bold uppercase">
            <ExternalLink className="h-3 w-3" />
            <span>VIEW ORIGINAL RECORD</span>
          </button>
        )}
      </div>
    </div>
  );
}
