"use client";

import { Observation } from "@/lib/types";
import { Eye, Database, Clock, Compass, Activity } from "lucide-react";

interface ObservationInspectorProps {
  observations: Observation[];
  selectedId: string;
  onSelect: (id: string) => void;
}

export function ObservationInspector({
  observations,
  selectedId,
  onSelect
}: ObservationInspectorProps) {
  const selected = observations.find((o) => o.id === selectedId) || observations[0];

  return (
    <div className="rounded-xl bg-slate-900/60 border border-slate-800 font-mono overflow-hidden">
      <div className="p-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2 text-xs text-slate-200">
          <Database className="h-4 w-4 text-cyan-400" />
          <span className="uppercase tracking-wider">SOURCE OBSERVATIONS ({observations.length})</span>
        </div>
        <div className="text-[10px] text-slate-500">RAW TELEMETRY AUDIT</div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-800">
        {/* Observation Selector List */}
        <div className="max-h-72 overflow-y-auto divide-y divide-slate-800/60">
          {observations.map((obs) => {
            const isSelected = obs.id === selectedId;
            return (
              <button
                key={obs.id}
                onClick={() => onSelect(obs.id)}
                className={`w-full text-left p-3 transition-colors flex items-center justify-between text-xs ${
                  isSelected
                    ? "bg-cyan-950/30 border-l-2 border-cyan-400 text-slate-100"
                    : "hover:bg-slate-800/40 text-slate-400"
                }`}
              >
                <div>
                  <div className="font-semibold text-slate-200 uppercase tracking-tight">{obs.type}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">
                    {obs.id} // {obs.source}
                  </div>
                </div>
                <div className="text-right">
                  <span
                    className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                      obs.confidence >= 90
                        ? "bg-emerald-950/50 text-emerald-400 border border-emerald-800/50"
                        : "bg-cyan-950/50 text-cyan-400 border border-cyan-800/50"
                    }`}
                  >
                    {obs.confidence}%
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Observation Details Panel */}
        <div className="p-4 md:col-span-2 space-y-4">
          {selected ? (
            <>
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-[10px] text-cyan-400 tracking-wider uppercase">
                    RECORD ID: {selected.id}
                  </span>
                  <h4 className="text-sm font-bold text-slate-100 uppercase">{selected.type}</h4>
                </div>
                <div className="flex items-center gap-2 text-xs text-slate-400">
                  <Clock className="h-3.5 w-3.5" />
                  <span className="text-[11px]">{selected.observedAt}</span>
                </div>
              </div>

              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                <div className="p-2.5 rounded bg-slate-950/60 border border-slate-800/80">
                  <div className="text-[10px] text-slate-500 uppercase">Provider / Source</div>
                  <div className="text-slate-200 font-semibold mt-0.5 uppercase">{selected.source}</div>
                </div>
                <div className="p-2.5 rounded bg-slate-950/60 border border-slate-800/80">
                  <div className="text-[10px] text-slate-500 uppercase">Measured Value</div>
                  <div className="text-cyan-400 font-bold mt-0.5">
                    {typeof selected.value === "object"
                      ? JSON.stringify(selected.value)
                      : `${selected.value} ${selected.unit || ""}`}
                  </div>
                </div>
                <div className="p-2.5 rounded bg-slate-950/60 border border-slate-800/80 col-span-2 sm:col-span-1">
                  <div className="text-[10px] text-slate-500 uppercase">Source Identifier</div>
                  <div className="text-slate-300 font-mono text-[11px] truncate mt-0.5">
                    {selected.sourceId || "OAH-STD-992"}
                  </div>
                </div>
              </div>

              {selected.notes && (
                <div className="p-3 rounded bg-slate-950/40 border border-slate-800 text-xs text-slate-400">
                  <span className="text-[10px] text-slate-500 uppercase block mb-1">Telemetry Notes</span>
                  {selected.notes}
                </div>
              )}
            </>
          ) : (
            <div className="text-xs text-slate-500 py-8 text-center">No observation selected.</div>
          )}
        </div>
      </div>
    </div>
  );
}
