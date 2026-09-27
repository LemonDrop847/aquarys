"use client";

import { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { Site } from "@/lib/types";

interface NetworkMapProps {
  sites: Site[];
  selectedSiteId: string | null;
  onSelectSite: (id: string) => void;
  className?: string;
}

export function NetworkMap({
  sites,
  selectedSiteId,
  onSelectSite,
  className = "",
}: NetworkMapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<{ [key: string]: maplibregl.Marker }>({});
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    try {
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: {
          version: 8,
          sources: {
            "carto-dark": {
              type: "raster",
              tiles: [
                "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
                "https://b.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
                "https://c.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
                "https://d.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}@2x.png",
              ],
              tileSize: 256,
              attribution:
                '&copy; <a href="https://carto.com/">CARTO</a> &copy; OpenStreetMap',
            },
          },
          layers: [
            {
              id: "carto-dark-layer",
              type: "raster",
              source: "carto-dark",
              minzoom: 0,
              maxzoom: 19,
            },
          ],
        },
        center: [3.0, 48.0], // Center of Western Europe
        zoom: 4.2,
        attributionControl: false,
      });

      map.current.addControl(
        new maplibregl.NavigationControl({ showCompass: false }),
        "bottom-right"
      );

      map.current.on("load", () => {
        setMapLoaded(true);
      });
    } catch (err) {
      console.error("Failed to initialize MapLibre map:", err);
    }

    return () => {
      if (map.current) {
        map.current.remove();
        map.current = null;
      }
    };
  }, []);

  // Update Markers
  useEffect(() => {
    if (!map.current || !mapLoaded) return;

    // Clear old markers
    Object.values(markersRef.current).forEach((m) => m.remove());
    markersRef.current = {};

    sites.forEach((site) => {
      const isSelected = site.id === selectedSiteId;

      const el = document.createElement("div");
      el.className = "cursor-pointer group relative";
      el.innerHTML = `
        <div class="relative flex items-center justify-center">
          <div class="w-8 h-8 rounded-full ${
            isSelected
              ? "bg-cyan-500/30 border-2 border-cyan-400 scale-125 shadow-[0_0_15px_rgba(6,182,212,0.8)]"
              : "bg-slate-900/90 border border-slate-700 group-hover:border-cyan-400 group-hover:scale-110"
          } transition-all duration-300 flex items-center justify-center backdrop-blur-sm">
            <span class="font-mono text-[10px] font-bold ${
              isSelected ? "text-cyan-200" : "text-slate-300 group-hover:text-white"
            }">${site.code}</span>
          </div>
          ${
            isSelected
              ? '<div class="absolute -inset-1 rounded-full bg-cyan-400/20 animate-ping pointer-events-none"></div>'
              : ""
          }
        </div>
      `;

      el.addEventListener("click", () => {
        onSelectSite(site.id);
      });

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([site.longitude, site.latitude])
        .addTo(map.current!);

      markersRef.current[site.id] = marker;
    });
  }, [sites, selectedSiteId, mapLoaded, onSelectSite]);

  // Pan to selected site
  useEffect(() => {
    if (!map.current || !selectedSiteId) return;
    const site = sites.find((s) => s.id === selectedSiteId);
    if (site) {
      map.current.flyTo({
        center: [site.longitude, site.latitude],
        zoom: 7,
        duration: 1200,
        essential: true,
      });
    }
  }, [selectedSiteId, sites]);

  return (
    <div className={`relative w-full h-full min-h-[400px] ${className}`}>
      <div ref={mapContainer} className="w-full h-full" />
      <div className="absolute top-4 left-4 pointer-events-none z-10 flex items-center gap-2 bg-slate-950/80 backdrop-blur-md px-3 py-1.5 rounded-lg border border-slate-800 text-[11px] font-mono text-slate-300">
        <span className="h-2 w-2 rounded-full bg-cyan-400 animate-pulse" />
        <span>MAPLIBRE TELEMETRY LAYER</span>
      </div>
    </div>
  );
}
