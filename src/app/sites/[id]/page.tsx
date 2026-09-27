"use client";

import { useParams } from "next/navigation";
import { useSites } from "@/hooks/use-sites";
import { StreamFingerprint } from "@/components/sites/StreamFingerprintView";
import { Timeline } from "@/components/sites/TimelineView";
import { ActionQuicklinks } from "@/components/sites/ActionQuicklinks";
import { MapPin, ArrowLeft } from "lucide-react";
import Link from "next/link";

export default function SiteIntelligencePage() {
  const params = useParams();
  const id = params?.id as string;
  const { data: sites = [], isLoading } = useSites();
  const site = sites.find((s) => s.id === id);

  if (isLoading) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-[#06090e]">
        <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!site) {
    return <div className="p-8 text-center font-mono text-slate-400 min-h-[100dvh] bg-[#06090e]">Site not found.</div>;
  }

  return (
    <div className="min-h-[100dvh] bg-[#06090e] text-slate-100 pb-20">
      <div className="sticky top-0 z-30 bg-[#080d14]/80 backdrop-blur-md border-b border-slate-800">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/sites" className="p-2 rounded bg-slate-900 border border-slate-800 hover:bg-slate-800 transition-colors">
            <ArrowLeft className="h-4 w-4 text-slate-300" />
          </Link>
          <div>
            <div className="text-[10px] font-mono text-cyan-400 tracking-wider mb-1">
              SITE INTELLIGENCE // {site.code}
            </div>
            <h1 className="text-xl font-bold font-mono">{site.name}</h1>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          {/* Identity & Coverage */}
          <div className="grid grid-cols-2 gap-4">
            <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800 flex flex-col justify-center">
              <div className="flex items-center gap-2 text-xs text-slate-400 font-mono mb-2">
                <MapPin className="h-3.5 w-3.5" /> Location
              </div>
              <div className="text-sm">{site.region}</div>
              <div className="text-xs text-slate-500">{site.country}</div>
            </div>
            <div className="p-5 rounded-xl bg-slate-900/40 border border-slate-800 flex flex-col justify-center">
              <div className="text-[10px] font-mono text-slate-400 uppercase tracking-wider mb-2">
                Evidence Coverage
              </div>
              <div className="text-3xl font-bold text-emerald-400">{site.evidenceCoverage}%</div>
              <div className="text-xs text-slate-500 mt-1">{site.observationCount} Observations</div>
            </div>
          </div>

          {/* Fingerprint */}
          <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-mono text-sm uppercase tracking-wider text-slate-200">8-Axis Fingerprint</h2>
              <span className="text-[10px] font-mono px-2 py-1 bg-cyan-950/30 text-cyan-400 border border-cyan-900/50 rounded">
                VALIDATED
              </span>
            </div>
            <StreamFingerprint siteId={site.id} />
          </div>

          {/* Timeline */}
          <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800">
            <Timeline siteId={site.id} />
          </div>
        </div>

        <div className="space-y-6">
          <div className="p-6 rounded-xl bg-slate-900/40 border border-slate-800">
            <h2 className="font-mono text-sm uppercase tracking-wider text-slate-200 mb-4">Actions</h2>
            <ActionQuicklinks siteId={site.id} />
          </div>

          <div className="p-5 rounded-xl bg-amber-950/10 border border-amber-900/30">
            <div className="text-[10px] font-mono text-amber-500 uppercase tracking-wider mb-2">
              Knowledge Gaps
            </div>
            <div className="text-2xl font-bold text-amber-400 mb-1">{site.knowledgeGaps}</div>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              Missing citizen observations and recent chemical confirmation. Recommend dispatching mission.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
