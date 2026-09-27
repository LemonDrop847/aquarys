"use client";

import { useState } from "react";
import { MapPin, Filter, Compass, ChevronRight } from "lucide-react";
import Link from "next/link";
import { motion } from "motion/react";
import { DemoBadge } from "@/components/ui/DemoBadge";
import { NetworkMap } from "@/components/map/NetworkMap";
import { useSites } from "@/hooks/use-sites";

export default function SitesPage() {
  const { data: sites = [], isLoading } = useSites();
  const [selectedSiteId, setSelectedSiteId] = useState<string | null>(null);
  const [filterRegion, setFilterRegion] = useState<string>("all");

  const regions = ["all", ...Array.from(new Set(sites.map((s) => s.region)))];

  const filteredSites =
    filterRegion === "all"
      ? sites
      : sites.filter((s) => s.region === filterRegion);

  const selectedSite = sites.find((s) => s.id === selectedSiteId);

  return (
    <div className="relative min-h-[100dvh] bg-[#06090e] text-slate-100">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[300px] bg-gradient-to-b from-cyan-950/20 via-blue-950/10 to-transparent blur-3xl pointer-events-none -z-10" />

      {/* Header */}
      <section className="border-b border-slate-800/60 bg-[#080d14]/60 backdrop-blur-sm sticky top-0 z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <DemoBadge />
                <span className="font-mono text-xs text-cyan-400 tracking-wider uppercase flex items-center gap-1.5">
                  <Compass className="h-3.5 w-3.5" />
                  ENVIRONMENTAL NETWORK
                </span>
              </div>
              <h1 className="font-mono text-2xl sm:text-3xl font-bold text-white">
                European Urban Stream Network
              </h1>
            </div>

            <div className="flex items-center gap-3">
              <Filter className="h-4 w-4 text-slate-400" />
              <select
                value={filterRegion}
                onChange={(e) => setFilterRegion(e.target.value)}
                className="px-3 py-2 rounded bg-slate-900/80 border border-slate-800 text-slate-200 font-mono text-xs hover:border-cyan-500/50 transition-colors focus:outline-none focus:border-cyan-500"
              >
                {regions.map((r) => (
                  <option key={r} value={r}>
                    {r === "all" ? "ALL REGIONS" : r.toUpperCase()}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {!isLoading && (
            <div className="mt-4 flex items-center gap-6 text-xs font-mono text-slate-400">
              <span>
                <span className="text-cyan-400 font-semibold">
                  {filteredSites.length}
                </span>{" "}
                MONITORED SITES
              </span>
              <span>
                <span className="text-emerald-400 font-semibold">
                  {filteredSites.reduce((sum, s) => sum + s.observationCount, 0)}
                </span>{" "}
                OBSERVATIONS
              </span>
            </div>
          )}
        </div>
      </section>

      {/* Map + Side Panel */}
      <div className="flex flex-col lg:flex-row h-[calc(100dvh-140px)]">
        {/* Map */}
        <div className="flex-1 relative">
          {isLoading ? (
            <div className="absolute inset-0 flex items-center justify-center bg-slate-950/60">
              <div className="text-center space-y-3">
                <div className="w-8 h-8 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin mx-auto" />
                <p className="font-mono text-xs text-slate-400 uppercase tracking-wider">
                  Loading network
                </p>
              </div>
            </div>
          ) : (
            <NetworkMap
              sites={filteredSites}
              selectedSiteId={selectedSiteId}
              onSelectSite={setSelectedSiteId}
            />
          )}
        </div>

        {/* Side Panel */}
        <motion.aside
          initial={false}
          animate={{
            width: selectedSite ? "auto" : "0px",
            opacity: selectedSite ? 1 : 0,
          }}
          transition={{ duration: 0.3 }}
          className="border-l border-slate-800/80 bg-[#04060a] overflow-hidden"
        >
          {selectedSite && (
            <div className="w-[360px] p-6 space-y-6 overflow-y-auto h-full">
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-2xl font-bold text-cyan-400">
                    {selectedSite.code}
                  </span>
                  <button
                    onClick={() => setSelectedSiteId(null)}
                    className="text-slate-400 hover:text-slate-200 transition-colors"
                    aria-label="Close panel"
                  >
                    ✕
                  </button>
                </div>
                <h2 className="text-xl font-bold text-slate-100">
                  {selectedSite.name}
                </h2>
                <div className="flex items-center gap-2 text-xs text-slate-400 font-mono">
                  <MapPin className="h-3.5 w-3.5" />
                  <span>
                    {selectedSite.region}, {selectedSite.country}
                  </span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 rounded bg-slate-900/60 border border-slate-800/60">
                  <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1">
                    Evidence Coverage
                  </div>
                  <div className="text-2xl font-bold text-emerald-400">
                    {selectedSite.evidenceCoverage}%
                  </div>
                </div>
                <div className="p-3 rounded bg-slate-900/60 border border-slate-800/60">
                  <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-1">
                    Observations
                  </div>
                  <div className="text-2xl font-bold text-cyan-400">
                    {selectedSite.observationCount}
                  </div>
                </div>
              </div>

              <div className="p-4 rounded bg-slate-900/40 border border-slate-800/40 space-y-2">
                <div className="flex items-center justify-between text-xs font-mono">
                  <span className="text-slate-300">Knowledge Gaps</span>
                  <span
                    className={`font-semibold ${
                      selectedSite.knowledgeGaps > 4
                        ? "text-amber-400"
                        : "text-slate-400"
                    }`}
                  >
                    {selectedSite.knowledgeGaps} IDENTIFIED
                  </span>
                </div>
                <div className="text-[11px] text-slate-400">
                  Last observed:{" "}
                  {new Date(selectedSite.lastObserved).toLocaleDateString("en-GB", {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                  })}
                </div>
              </div>

              <Link
                href={`/sites/${selectedSite.id}`}
                className="w-full py-3 px-4 rounded-lg bg-cyan-500 text-slate-950 font-mono text-sm font-semibold hover:bg-cyan-400 transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)] active:scale-95 flex items-center justify-center gap-2"
              >
                <span>EXPLORE SITE INTELLIGENCE</span>
                <ChevronRight className="h-4 w-4" />
              </Link>

              <div className="pt-4 border-t border-slate-800 space-y-2">
                <Link
                  href={`/trust?observationId=obs-${selectedSite.id}`}
                  className="w-full py-2 px-3 rounded bg-slate-800/80 hover:bg-slate-700 text-slate-200 font-mono text-xs transition-colors flex items-center justify-between"
                >
                  <span>Evidence X-RAY</span>
                  <ChevronRight className="h-3.5 w-3.5" />
                </Link>
                <Link
                  href={`/twins?siteId=${selectedSite.id}`}
                  className="w-full py-2 px-3 rounded bg-slate-800/80 hover:bg-slate-700 text-slate-200 font-mono text-xs transition-colors flex items-center justify-between"
                >
                  <span>Find Twins</span>
                  <ChevronRight className="h-3.5 w-3.5" />
                </Link>
                <Link
                  href={`/oracle?siteId=${selectedSite.id}`}
                  className="w-full py-2 px-3 rounded bg-slate-800/80 hover:bg-slate-700 text-slate-200 font-mono text-xs transition-colors flex items-center justify-between"
                >
                  <span>Ask Oracle</span>
                  <ChevronRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          )}
        </motion.aside>
      </div>
    </div>
  );
}
