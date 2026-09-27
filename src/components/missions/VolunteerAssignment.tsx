"use client";

import { MissionTask } from "@/lib/types";
import { User, Clock, MapPin, Zap, CheckCircle2, ChevronRight } from "lucide-react";

interface VolunteerAssignmentProps {
  tasks: MissionTask[];
  selectedTaskId?: string;
  onSelectTask: (taskId: string) => void;
}

export function VolunteerAssignment({
  tasks,
  selectedTaskId,
  onSelectTask
}: VolunteerAssignmentProps) {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="p-8 text-center text-slate-500 font-mono text-xs border border-slate-800 rounded-xl bg-slate-900/40">
        NO VOLUNTEER ASSIGNMENTS GENERATED
      </div>
    );
  }

  return (
    <div className="space-y-3 font-mono">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center gap-2 text-xs font-bold text-slate-200 uppercase tracking-wider">
          <User className="h-4 w-4 text-cyan-400" />
          <span>OPTIMIZED VOLUNTEER DISPATCH SCHEDULE ({tasks.length})</span>
        </div>
        <span className="text-[10px] text-slate-500 uppercase">
          SEQUENCED BY GAIN DENSITY
        </span>
      </div>

      <div className="space-y-2.5">
        {tasks.map((task, index) => {
          const isSelected = selectedTaskId === task.id;
          const priorityColor =
            task.priority === "high"
              ? "text-rose-400 border-rose-800/60 bg-rose-950/40"
              : task.priority === "medium"
              ? "text-amber-400 border-amber-800/60 bg-amber-950/40"
              : "text-slate-400 border-slate-800 bg-slate-900/60";

          return (
            <div
              key={task.id}
              onClick={() => onSelectTask(task.id)}
              className={`p-4 rounded-xl border transition-all cursor-pointer ${
                isSelected
                  ? "bg-slate-900/90 border-cyan-500/80 shadow-lg shadow-cyan-500/10 ring-1 ring-cyan-500/30"
                  : "bg-slate-900/50 border-slate-800 hover:border-slate-700 hover:bg-slate-900/80"
              }`}
            >
              <div className="flex items-start justify-between gap-3 mb-2">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`w-7 h-7 rounded-lg flex items-center justify-center font-bold text-xs border ${
                      isSelected
                        ? "bg-cyan-500 text-slate-950 border-cyan-400 shadow-md shadow-cyan-500/30"
                        : "bg-slate-800 text-cyan-400 border-slate-700"
                    }`}
                  >
                    V{index + 1}
                  </div>
                  <div>
                    <div className="text-xs font-bold text-slate-100 flex items-center gap-2">
                      <span>{task.volunteerName}</span>
                      <span
                        className={`text-[9px] uppercase px-1.5 py-0.5 rounded border ${priorityColor}`}
                      >
                        {task.priority} PRIORITY
                      </span>
                    </div>
                    <div className="text-[11px] text-cyan-400 font-semibold flex items-center gap-1.5 mt-0.5">
                      <MapPin className="h-3 w-3 text-cyan-500" />
                      <span>{task.siteName}</span>
                      <span className="text-slate-500 text-[10px]">({task.siteCode})</span>
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-[10px] text-slate-500 uppercase">Information Gain</div>
                  <div className="text-xs font-bold text-emerald-400 flex items-center justify-end gap-1">
                    <Zap className="h-3 w-3 fill-emerald-400/20" />
                    <span>+{(task.informationGain * 100).toFixed(0)}%</span>
                  </div>
                </div>
              </div>

              {/* Task detail */}
              <div className="mt-2.5 p-2.5 rounded-lg bg-slate-950/80 border border-slate-800/80 text-xs text-slate-300">
                <div className="text-[10px] text-slate-400 uppercase font-bold mb-1 flex items-center gap-1">
                  <CheckCircle2 className="h-3 w-3 text-cyan-400" />
                  <span>ACTION PROTOCOL:</span>
                </div>
                <p className="text-[11px] leading-relaxed text-slate-200">{task.observation}</p>
              </div>

              {/* Footer metadata */}
              <div className="mt-3 flex items-center justify-between text-[10px] text-slate-500 pt-2 border-t border-slate-800/60">
                <div className="flex items-center gap-4">
                  <span className="flex items-center gap-1">
                    <Clock className="h-3 w-3 text-slate-400" />
                    <span>Est. {task.estimatedDurationMinutes} mins</span>
                  </span>
                  <span className="text-slate-400 truncate max-w-[200px]">
                    📍 {task.location}
                  </span>
                </div>

                <div className="flex items-center gap-1 text-cyan-400 font-bold group">
                  <span>{isSelected ? "FOCUSED ON MAP" : "VIEW ON MAP"}</span>
                  <ChevronRight className="h-3 w-3 transition-transform group-hover:translate-x-0.5" />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
