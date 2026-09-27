"use client";

import { useEffect, useRef } from "react";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Mission, MissionTask } from "@/lib/types";
import { Map as MapIcon, AlertCircle } from "lucide-react";

interface MissionMapProps {
  mission: Mission;
  selectedTaskId?: string;
  onTaskSelect?: (taskId: string) => void;
}

export function MissionMap({ mission, selectedTaskId, onTaskSelect }: MissionMapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<globalThis.Map<string, maplibregl.Marker>>(new globalThis.Map<string, maplibregl.Marker>());

  useEffect(() => {
    if (!mapContainer.current) return;

    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: "https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json",
      center: [3.0, 48.0],
      zoom: 4,
      attributionControl: false
    });

    map.current.addControl(new maplibregl.NavigationControl(), "bottom-right");

    return () => {
      map.current?.remove();
    };
  }, []);

  useEffect(() => {
    if (!map.current) return;

    // Clear existing markers
    markersRef.current.forEach((marker) => marker.remove());
    markersRef.current.clear();

    // Add markers for each task
    mission.tasks?.forEach((task) => {
      if (!task.latitude || !task.longitude) return;

      const el = document.createElement("div");
      el.className = `w-10 h-10 rounded-full flex items-center justify-center cursor-pointer transition-all ${
        selectedTaskId === task.id
          ? "bg-cyan-500 shadow-lg shadow-cyan-500/50 scale-125"
          : "bg-slate-700 hover:bg-slate-600"
      }`;

      const isHighPriority = task.priority === "high";
      const innerColor = isHighPriority ? "text-rose-300" : "text-cyan-300";

      el.innerHTML = `
        <span class="text-xs font-bold ${innerColor}">
          ${task.volunteerId || "V"}
        </span>
      `;

      el.addEventListener("click", () => {
        if (onTaskSelect) onTaskSelect(task.id);
      });

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([task.longitude, task.latitude])
        .addTo(map.current!);

      markersRef.current.set(task.id, marker);
    });

    // Fit bounds if tasks exist
    if (mission.tasks && mission.tasks.length > 0 && markersRef.current.size > 0) {
      const bounds = new maplibregl.LngLatBounds();
      mission.tasks.forEach((task) => {
        if (task.latitude && task.longitude) {
          bounds.extend([task.longitude, task.latitude]);
        }
      });
      map.current.fitBounds(bounds, { padding: 80, maxZoom: 12 });
    }
  }, [mission.tasks, selectedTaskId, onTaskSelect]);

  if (!mission.tasks || mission.tasks.length === 0) {
    return (
      <div className="w-full h-[400px] rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-center">
        <div className="text-center space-y-3">
          <AlertCircle className="h-8 w-8 text-slate-500 mx-auto" />
          <p className="text-xs text-slate-400 font-mono uppercase">No assignments yet</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-[400px] rounded-xl overflow-hidden border border-slate-800 shadow-xl">
      <div ref={mapContainer} className="absolute inset-0 bg-slate-950" />

      {/* Legend */}
      <div className="absolute top-4 left-4 bg-slate-900/90 border border-slate-800 rounded-lg p-3 font-mono text-xs space-y-2 max-w-xs">
        <div className="flex items-center gap-2 text-cyan-400 font-bold uppercase tracking-wider">
          <MapIcon className="h-3 w-3" />
          <span>Mission Coverage</span>
        </div>

        <div className="space-y-1.5 text-slate-300">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-full bg-cyan-500 shadow-lg shadow-cyan-500/50 border border-cyan-400" />
            <span className="text-[10px]">Selected Assignment</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-full bg-rose-500 border border-rose-400" />
            <span className="text-[10px]">High Priority</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-full bg-slate-700 border border-slate-600" />
            <span className="text-[10px]">Standard Priority</span>
          </div>
        </div>

        <div className="pt-2 border-t border-slate-700 text-[10px] text-slate-400">
          {mission.tasks.length} assignments across {new Set(mission.tasks.map((t) => t.siteId)).size} sites
        </div>
      </div>

      {/* Attribution */}
      <div className="absolute bottom-2 right-2 text-[9px] text-slate-500">
        © OpenStreetMap contributors
      </div>
    </div>
  );
}
