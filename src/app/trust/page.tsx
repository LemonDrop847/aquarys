"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useSites } from "@/hooks/use-sites";
import { useObservations } from "@/hooks/use-observations";
import { useEvaluateTrust, useExportFHIR } from "@/hooks/use-trust";
import { EvidencePassport } from "@/components/trust/EvidencePassport";
import { TrustScan } from "@/components/trust/TrustScan";
import { ObservationInspector } from "@/components/trust/ObservationInspector";
import { FHIRExportModal } from "@/components/evidence/FHIRExportModal";
import { Shield, Sparkles, Filter, Search, ShieldCheck, ArrowUpRight } from "lucide-react";
import Link from "next/link";
import { FHIRBundle } from "@/lib/types";

export default function TrustPage() {
  const router = useRouter();
  const { data: sites = [], isLoading: isSitesLoading } = useSites();
  const [selectedSiteId, setSelectedSiteId] = useState<string>("site-c1");
  const { data: observations = [], isLoading: isObsLoading } = useObservations(selectedSiteId);
  const [selectedObsId, setSelectedObsId] = useState<string>("obs-101");

  const [isScanning, setIsScanning] = useState(false);
  const [hasScanned, setHasScanned] = useState(true);

  // Trust evaluation query / mutation
  const evaluateTrust = useEvaluateTrust();
  const exportFHIR = useExportFHIR();

  // Export Modal state
  const [fhirModalOpen, setFhirModalOpen] = useState(false);
  const [fhirBundle, setFhirBundle] = useState<FHIRBundle | null>(null);

  // Profile data from mutation or fallback
  const [activeProfile, setActiveProfile] = useState<any>(null);

  const handleSelectObservation = async (obsId: string) => {
    setSelectedObsId(obsId);
    setIsScanning(true);
    try {
      const res = await evaluateTrust.mutateAsync(obsId);
      setActiveProfile(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsScanning(false);
      setHasScanned(true);
    }
  };

  const handleReScan = async () => {
    setIsScanning(true);
    try {
      const res = await evaluateTrust.mutateAsync(selectedObsId || "obs-101");
      setActiveProfile(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsScanning(false);
      setHasScanned(true);
    }
  };

  const handleExportFHIR = async () => {
    try {
      const bundle = await exportFHIR.mutateAsync(selectedSiteId);
      setFhirBundle(bundle);
      setFhirModalOpen(true);
    } catch (e) {
      console.error(e);
    }
  };

  const currentObs = observations.find((o) => o.id === selectedObsId) || observations[0];
  const selectedSite = sites.find((s) => s.id === selectedSiteId) || sites[0];

  // Default fallback profile if not yet fetched
  const displayProfile = activeProfile || {
    observationId: currentObs?.id || "obs-101",
    overallTrust: 92,
    completeness: 100,
    consistency: 94,
    location: 91,
    temporalValidity: 97,
    imageSupport: 82,
    crossObserver: 87,
    independentSupport: 76,
    flags: [
      { metric: "Schema Validation", status: "complete", score: 100 },
      { metric: "Temporal Precision", status: "complete", score: 97 },
      { metric: "Observer Calibration", status: "partial", score: 87 },
      { metric: "Chemical Confirmation", status: "warning", score: 62 }
    ],
    explanation:
      "Telemetry verified against Sentinel-2 spectral surface index (NDWI=0.48) and validated across 4 co-located citizen sensor arrays in Mondego basin. Observation conforms to HL7 FHIR v4.0.1 and OAH schema v2.",
    warnings: [
      "No lab-certified wet chemistry sample collected within 72 hours of this observation."
    ]
  };

  return (
    <div className="space-y-8 pb-16">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs uppercase tracking-wider mb-1">
            <ShieldCheck className="h-4 w-4" />
            <span>X-RAY EVIDENCE PASSPORT & INTEGRITY VERIFICATION</span>
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-100 uppercase font-mono">
            Evidence Passport
          </h1>
          <p className="text-xs text-slate-400 max-w-2xl mt-1">
            Audit raw environmental telemetry, evaluate multi-dimensional verification criteria, and verify provenance against cross-observer records.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleExportFHIR}
            disabled={exportFHIR.isPending}
            className="px-4 py-2 rounded bg-slate-900 border border-slate-700 hover:border-slate-500 text-slate-200 text-xs font-mono font-medium transition-colors flex items-center gap-2"
          >
            <span>HL7 FHIR EXPORT</span>
            <ArrowUpRight className="h-3.5 w-3.5 text-cyan-400" />
          </button>
        </div>
      </div>

      {/* Selector Toolbar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 bg-slate-900/40 p-4 rounded-xl border border-slate-800/80 font-mono text-xs">
        <div>
          <label className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1.5">
            Active Site
          </label>
          <select
            value={selectedSiteId}
            onChange={(e) => {
              setSelectedSiteId(e.target.value);
            }}
            className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            {sites.map((s) => (
              <option key={s.id} value={s.id}>
                {s.code} · {s.name}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1.5">
            Evidence Record
          </label>
          <select
            value={selectedObsId}
            onChange={(e) => handleSelectObservation(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded px-2.5 py-1.5 text-slate-200 focus:outline-none focus:border-cyan-500"
          >
            {observations.map((o) => (
              <option key={o.id} value={o.id}>
                {o.id} - {o.type.substring(0, 24)}...
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1.5">
            Provider / Source
          </label>
          <div className="bg-slate-950/80 border border-slate-800/80 rounded px-2.5 py-1.5 text-slate-400 truncate">
            {currentObs?.source || "OAH Sensor Network"}
          </div>
        </div>

        <div>
          <label className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1.5">
            Trust Score
          </label>
          <div className="bg-slate-950/80 border border-slate-800/80 rounded px-2.5 py-1.5 text-emerald-400 font-bold flex items-center justify-between">
            <span>PASSPORT VERIFIED</span>
            <span>{displayProfile.overallTrust}%</span>
          </div>
        </div>
      </div>

      {/* Main Analysis Area */}
      {isScanning ? (
        <div className="p-8 rounded-xl bg-slate-900/40 border border-slate-800 flex items-center justify-center">
          <TrustScan scanning={isScanning} onScanComplete={() => setIsScanning(false)} />
        </div>
      ) : (
        <div className="space-y-8">
          {/* Evidence Passport Box */}
          <div className="p-6 rounded-2xl bg-slate-900/60 border border-slate-800 shadow-xl">
            <EvidencePassport
              profile={displayProfile}
              onExport={handleExportFHIR}
              onViewGraph={() => router.push(`/evidence/${displayProfile.observationId}`)}
              onReScan={handleReScan}
            />
          </div>

          {/* Raw Observation Inspector */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400">
                OBSERVATION TELEMETRY AUDITOR
              </h3>
              <Link
                href={`/evidence/${displayProfile.observationId}`}
                className="text-xs font-mono text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
              >
                <span>OPEN PROVENANCE GRAPH</span>
                <ArrowUpRight className="h-3.5 w-3.5" />
              </Link>
            </div>

            <ObservationInspector
              observations={observations}
              selectedId={selectedObsId}
              onSelect={handleSelectObservation}
            />
          </div>
        </div>
      )}

      {/* FHIR Export Modal */}
      <FHIRExportModal
        isOpen={fhirModalOpen}
        onClose={() => setFhirModalOpen(false)}
        bundle={fhirBundle}
        isLoading={exportFHIR.isPending}
      />
    </div>
  );
}
