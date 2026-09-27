"use client";

import { useState } from "react";
import { useSites } from "@/hooks/use-sites";
import { useTwins, useCompareSites } from "@/hooks/use-twins";
import { TwinCard } from "@/components/twins/TwinCard";
import { TwinSearchAnimation } from "@/components/twins/TwinSearchAnimation";
import { TwinComparisonView } from "@/components/twins/TwinComparisonView";
import {
  GitCompare,
  Search,
  Sparkles,
  ArrowRight,
  RefreshCw,
  SlidersHorizontal,
  Compass,
  Layers
} from "lucide-react";
import Link from "next/link";

export default function TwinsPage() {
  const { data: sites = [] } = useSites();
  const [selectedSiteId, setSelectedSiteId] = useState<string>("site-c1");
  const [selectedTwinId, setSelectedTwinId] = useState<string>("site-g7");

  const [isSearching, setIsSearching] = useState(false);
  const [viewMode, setViewMode] = useState<"discovery" | "comparison">("discovery");

  const { data: twins = [], isLoading: isTwinsLoading, refetch: refetchTwins } = useTwins(
    selectedSiteId
  );
  const { data: comparison, isLoading: isComparisonLoading } = useCompareSites(
    selectedSiteId,
    selectedTwinId
  );

  const selectedSite = sites.find((s) => s.id === selectedSiteId) || sites[0];

  const handleStartSearch = () => {
    setIsSearching(true);
  };

  const handleSearchComplete = () => {
    setIsSearching(false);
  };

  const handleSelectTwin = (twinSiteId: string) => {
    setSelectedTwinId(twinSiteId);
    setViewMode("comparison");
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs uppercase tracking-wider mb-1">
            <GitCompare className="h-4 w-4" />
            <span>CROSS-BASIN COMPARATIVE INTELLIGENCE</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 uppercase font-mono">
            Ecological Twin Discovery
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl mt-1">
            Identify European stream basins sharing hydromorphic topology, biological signatures, and intervention history to transfer verified ecological solutions.
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <button
            onClick={() => setViewMode("discovery")}
            className={`px-3 py-1.5 rounded transition-colors ${
              viewMode === "discovery"
                ? "bg-cyan-500 text-slate-950 font-bold"
                : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200"
            }`}
          >
            TWIN CLUSTERS ({twins.length})
          </button>
          <button
            onClick={() => setViewMode("comparison")}
            className={`px-3 py-1.5 rounded transition-colors ${
              viewMode === "comparison"
                ? "bg-cyan-500 text-slate-950 font-bold"
                : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200"
            }`}
          >
            SPLIT COMPARISON
          </button>
        </div>
      </div>

      {/* Target Site Selection Bar */}
      <div className="p-4 rounded-xl bg-slate-900/40 border border-slate-800 font-mono text-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex flex-1 items-center gap-3">
          <div className="text-[10px] text-slate-500 uppercase tracking-wider shrink-0">
            TARGET STREAM:
          </div>
          <select
            value={selectedSiteId}
            onChange={(e) => {
              setSelectedSiteId(e.target.value);
              setIsSearching(true);
            }}
            className="bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500 max-w-xs font-semibold"
          >
            {sites.map((s) => (
              <option key={s.id} value={s.id}>
                {s.code} · {s.name} ({s.country})
              </option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleStartSearch}
            disabled={isSearching}
            className="px-4 py-2 rounded bg-cyan-500/10 border border-cyan-500/40 hover:bg-cyan-500/20 text-cyan-300 font-bold flex items-center gap-2 transition-colors"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isSearching ? "animate-spin" : ""}`} />
            <span>RE-SCAN TWIN VECTOR MATRIX</span>
          </button>
        </div>
      </div>

      {/* Searching State Overlay */}
      {isSearching ? (
        <div className="py-12">
          <TwinSearchAnimation
            isSearching={isSearching}
            onSearchComplete={handleSearchComplete}
            siteName={selectedSite?.name || "Target Stream"}
          />
        </div>
      ) : viewMode === "discovery" ? (
        /* Twin Discovery Grid */
        <div className="space-y-6 font-mono">
          <div className="flex items-center justify-between">
            <div className="text-xs text-slate-400 uppercase tracking-wider">
              HIGH-CONFIDENCE ECOLOGICAL TWINS FOR{" "}
              <span className="text-cyan-400 font-bold">{selectedSite?.name}</span>
            </div>
            <div className="text-[10px] text-slate-500">
              MINIMUM SIMILARITY THRESHOLD: 80%
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {twins.map((twin) => (
              <TwinCard
                key={twin.siteId}
                twin={twin}
                isSelected={selectedTwinId === twin.siteId}
                onSelect={() => handleSelectTwin(twin.siteId)}
              />
            ))}
          </div>

          {/* Bottom Quick Action Box */}
          <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="space-y-1 text-center sm:text-left">
              <div className="text-xs font-bold text-slate-200 uppercase">
                Need automated cross-twin remediation advice?
              </div>
              <p className="text-xs text-slate-400">
                Run an environmental intelligence query using multi-site comparative trajectories.
              </p>
            </div>
            <Link
              href={`/oracle?siteId=${selectedSiteId}`}
              className="px-4 py-2 rounded bg-cyan-500 text-slate-950 font-bold text-xs uppercase tracking-wider hover:bg-cyan-400 transition-colors flex items-center gap-2"
            >
              <span>ASK ORACLE FOR TWIN INSIGHTS</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        </div>
      ) : (
        /* Twin Split Comparison View */
        <div className="space-y-6">
          <div className="flex items-center justify-between font-mono">
            <button
              onClick={() => setViewMode("discovery")}
              className="text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1.5"
            >
              <span>← BACK TO TWIN CLUSTERS</span>
            </button>
            <div className="text-[10px] text-slate-500">
              COMPARING {selectedSite?.code} VS {comparison?.siteB.code}
            </div>
          </div>

          {comparison ? (
            <TwinComparisonView comparison={comparison} />
          ) : (
            <div className="py-20 text-center font-mono text-xs text-slate-500">
              Loading stream comparison data...
            </div>
          )}
        </div>
      )}
    </div>
  );
}
