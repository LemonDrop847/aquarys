"use client";

import { useState } from "react";
import { Sliders, Users, Clock, Compass, Target, ArrowRight } from "lucide-react";
import { Site } from "@/lib/types";

interface MissionBuilderProps {
  sites: Site[];
  selectedSiteId: string;
  onSiteChange: (siteId: string) => void;
  onOptimize: (params: {
    siteId: string;
    objective: string;
    volunteerCount: number;
    timeAvailableMinutes: number;
  }) => void;
  isOptimizing: boolean;
}

export function MissionBuilder({
  sites,
  selectedSiteId,
  onSiteChange,
  onOptimize,
  isOptimizing
}: MissionBuilderProps) {
  const [objective, setObjective] = useState(
    "Resolve critical thermal and sediment knowledge gaps across target stream and tributaries"
  );
  const [volunteerCount, setVolunteerCount] = useState(5);
  const [timeAvailableMinutes, setTimeAvailableMinutes] = useState(60);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onOptimize({
      siteId: selectedSiteId,
      objective,
      volunteerCount,
      timeAvailableMinutes
    });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 space-y-6 font-mono shadow-2xl"
    >
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-2 text-cyan-400">
          <Sliders className="h-4 w-4" />
          <span className="text-xs font-bold uppercase tracking-wider">
            MISSION PARAMETER CONFIGURATION
          </span>
        </div>
        <span className="text-[10px] text-slate-500 uppercase">
          ALGORITHMIC OPTIMIZATION ENGINE
        </span>
      </div>

      <div className="space-y-4">
        {/* Target Site */}
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Compass className="h-3 w-3 text-cyan-400" />
            <span>TARGET ENVIRONMENTAL REACH</span>
          </label>
          <select
            value={selectedSiteId}
            onChange={(e) => onSiteChange(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 transition-colors"
          >
            {sites.map((s) => (
              <option key={s.id} value={s.id}>
                {s.code} · {s.name} ({s.country} · {s.knowledgeGaps} GAPS)
              </option>
            ))}
          </select>
        </div>

        {/* Objective */}
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Target className="h-3 w-3 text-cyan-400" />
            <span>MISSION OBJECTIVE</span>
          </label>
          <input
            type="text"
            value={objective}
            onChange={(e) => setObjective(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 transition-colors"
            placeholder="Enter mission objective or uncertainty target..."
          />
        </div>

        {/* Sliders: Volunteers & Time */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
          {/* Volunteer Count */}
          <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-3">
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-1.5 text-slate-300">
                <Users className="h-3.5 w-3.5 text-cyan-400" />
                <span className="text-[10px] font-bold uppercase">AVAILABLE SENSORS / VOLUNTEERS</span>
              </div>
              <span className="text-cyan-400 font-bold px-2 py-0.5 rounded bg-cyan-950 border border-cyan-800">
                {volunteerCount} SENSORS
              </span>
            </div>
            <input
              type="range"
              min={1}
              max={15}
              value={volunteerCount}
              onChange={(e) => setVolunteerCount(Number(e.target.value))}
              className="w-full accent-cyan-400 cursor-pointer"
            />
            <div className="flex justify-between text-[9px] text-slate-500">
              <span>1 SOLO</span>
              <span>8 SQUAD</span>
              <span>15 DEPLOYMENT</span>
            </div>
          </div>

          {/* Time Available */}
          <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-3">
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-1.5 text-slate-300">
                <Clock className="h-3.5 w-3.5 text-cyan-400" />
                <span className="text-[10px] font-bold uppercase">TIME WINDOW</span>
              </div>
              <span className="text-cyan-400 font-bold px-2 py-0.5 rounded bg-cyan-950 border border-cyan-800">
                {timeAvailableMinutes} MIN
              </span>
            </div>
            <input
              type="range"
              min={15}
              max={180}
              step={15}
              value={timeAvailableMinutes}
              onChange={(e) => setTimeAvailableMinutes(Number(e.target.value))}
              className="w-full accent-cyan-400 cursor-pointer"
            />
            <div className="flex justify-between text-[9px] text-slate-500">
              <span>15 MIN</span>
              <span>90 MIN</span>
              <span>180 MIN</span>
            </div>
          </div>
        </div>
      </div>

      <button
        type="submit"
        disabled={isOptimizing}
        className="w-full py-3 rounded-lg bg-cyan-500 text-slate-950 font-bold text-xs uppercase tracking-wider hover:bg-cyan-400 disabled:opacity-50 transition-all flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20"
      >
        {isOptimizing ? (
          <>
            <div className="h-3.5 w-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
            <span>CALCULATING MAX INFORMATION GAIN MATRIX...</span>
          </>
        ) : (
          <>
            <span>OPTIMIZE & DISPATCH SAMPLING ROUTE</span>
            <ArrowRight className="h-4 w-4" />
          </>
        )}
      </button>
    </form>
  );
}
