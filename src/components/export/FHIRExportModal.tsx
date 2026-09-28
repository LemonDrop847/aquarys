"use client";

import { useState } from "react";
import { FHIRBundle } from "@/lib/types";
import {
  FileCode,
  Download,
  Copy,
  Check,
  X,
  Layers,
  MapPin,
  Activity,
  ShieldCheck
} from "lucide-react";

interface FHIRExportModalProps {
  bundle: FHIRBundle;
  isOpen: boolean;
  onClose: () => void;
  title?: string;
}

interface FHIRResource {
  resourceType?: string;
  name?: string;
  id?: string;
  status?: string;
  effectiveDateTime?: string;
  code?: { text?: string };
  position?: { latitude?: number; longitude?: number };
  valueQuantity?: { value?: number; unit?: string };
  prediction?: Array<{
    outcome?: { text?: string };
    probabilityDecimal?: number;
    rationale?: string;
  }>;
  [key: string]: unknown;
}

export function FHIRExportModal({
  bundle,
  isOpen,
  onClose,
  title = "FHIR HL7 v4.0.1 Environmental Observation Bundle"
}: FHIRExportModalProps) {
  const [activeTab, setActiveTab] = useState<"summary" | "json">("summary");
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const jsonString = JSON.stringify(bundle, null, 2);

  const handleCopy = () => {
    navigator.clipboard.writeText(jsonString);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([jsonString], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `aquarys-fhir-bundle-${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-slate-950/80 backdrop-blur-md animate-in fade-in duration-200 font-mono">
      <div className="relative w-full max-w-4xl max-h-[90vh] bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-slate-950/60">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-cyan-950 border border-cyan-800 text-cyan-400">
              <FileCode className="h-5 w-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-100 uppercase tracking-wider">
                  {title}
                </h3>
                <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-950 border border-emerald-800 text-emerald-400 font-bold uppercase">
                  HL7 FHIR R4
                </span>
              </div>
              <p className="text-[11px] text-slate-400 mt-0.5">
                Standardized interoperable evidence package with cryptographic provenance
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Tab switcher */}
        <div className="flex items-center justify-between px-6 py-2.5 border-b border-slate-800 bg-slate-950/30 text-xs">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveTab("summary")}
              className={`px-3 py-1.5 rounded-md font-bold transition-all ${
                activeTab === "summary"
                  ? "bg-slate-800 text-cyan-400 border border-slate-700"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              STRUCTURED SUMMARY
            </button>
            <button
              onClick={() => setActiveTab("json")}
              className={`px-3 py-1.5 rounded-md font-bold transition-all ${
                activeTab === "json"
                  ? "bg-slate-800 text-cyan-400 border border-slate-700"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              RAW JSON PAYLOAD
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 font-bold text-xs flex items-center gap-1.5 transition-all"
            >
              {copied ? (
                <>
                  <Check className="h-3.5 w-3.5 text-emerald-400" />
                  <span className="text-emerald-400">COPIED</span>
                </>
              ) : (
                <>
                  <Copy className="h-3.5 w-3.5 text-slate-400" />
                  <span>COPY JSON</span>
                </>
              )}
            </button>
            <button
              onClick={handleDownload}
              className="px-3 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs flex items-center gap-1.5 transition-all shadow-md shadow-cyan-500/20"
            >
              <Download className="h-3.5 w-3.5" />
              <span>DOWNLOAD BUNDLE</span>
            </button>
          </div>
        </div>

        {/* Body content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {activeTab === "summary" ? (
            <div className="space-y-4">
              {/* Bundle Meta Overview */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Resource Type</div>
                  <div className="text-sm font-bold text-slate-200 mt-0.5">Bundle (collection)</div>
                </div>
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Total Entries</div>
                  <div className="text-sm font-bold text-cyan-400 mt-0.5">
                    {bundle.total || bundle.entry?.length || 0} RESOURCES
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-slate-950/60 border border-slate-800">
                  <div className="text-[10px] text-slate-500 uppercase">Export Timestamp</div>
                  <div className="text-sm font-bold text-slate-300 mt-0.5">
                    {bundle.meta?.lastUpdated
                      ? new Date(bundle.meta.lastUpdated).toLocaleString()
                      : new Date().toLocaleString()}
                  </div>
                </div>
              </div>

              {/* Resource Entries List */}
              <div className="space-y-3">
                <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
                  <Layers className="h-3.5 w-3.5 text-cyan-400" />
                  <span>PACKAGED FHIR ENTRIES ({bundle.entry?.length || 0})</span>
                </div>

                <div className="space-y-2.5">
                  {bundle.entry?.map((entry, idx) => {
                    const res = entry.resource as FHIRResource;
                    const rType = res.resourceType || "Unknown";

                    let icon = <Activity className="h-4 w-4 text-cyan-400" />;
                    let badgeColor = "bg-cyan-950 border-cyan-800 text-cyan-400";

                    if (rType === "Location") {
                      icon = <MapPin className="h-4 w-4 text-emerald-400" />;
                      badgeColor = "bg-emerald-950 border-emerald-800 text-emerald-400";
                    } else if (rType === "RiskAssessment") {
                      icon = <ShieldCheck className="h-4 w-4 text-purple-400" />;
                      badgeColor = "bg-purple-950 border-purple-800 text-purple-400";
                    }

                    return (
                      <div
                        key={idx}
                        className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 space-y-2"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2.5">
                            {icon}
                            <span className="text-xs font-bold text-slate-100">
                              {res.name || res.code?.text || res.id || `${rType} #${idx + 1}`}
                            </span>
                          </div>
                          <span
                            className={`text-[9px] font-bold uppercase px-2 py-0.5 rounded border ${badgeColor}`}
                          >
                            {rType}
                          </span>
                        </div>

                        {/* Specific details based on type */}
                        <div className="text-xs text-slate-400 space-y-1 pt-1 border-t border-slate-900">
                          {rType === "Location" && (
                            <div className="flex items-center justify-between text-[11px]">
                              <span>Coordinates: {(res.position as {latitude?: number})?.latitude}°, {(res.position as {longitude?: number})?.longitude}°</span>
                              <span className="text-emerald-400">Status: {(res.status as string) || "—"}</span>
                            </div>
                          )}
                          {rType === "Observation" && (
                            <div className="flex items-center justify-between text-[11px]">
                              <span>
                                Value: {res.valueQuantity?.value} {res.valueQuantity?.unit}
                              </span>
                              <span className="text-cyan-400">
                                Date: {res.effectiveDateTime ? new Date(res.effectiveDateTime).toLocaleDateString() : "—"}
                              </span>
                            </div>
                          )}
                          {rType === "RiskAssessment" && (
                            <div className="text-[11px]">
                              <p className="text-slate-300">
                                {res.prediction?.[0]?.outcome?.text}: {((res.prediction?.[0]?.probabilityDecimal || 0) * 100).toFixed(0)}%
                              </p>
                              <p className="text-[10px] text-slate-500 mt-0.5">
                                {res.prediction?.[0]?.rationale}
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          ) : (
            <div className="relative rounded-xl bg-slate-950 p-4 border border-slate-800">
              <pre className="text-xs text-cyan-300 overflow-x-auto leading-relaxed max-h-[500px]">
                {jsonString}
              </pre>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between text-[10px] text-slate-500">
          <span>OAH & WATER-DATA COMPLIANT JSON INTERCHANGE FORMAT</span>
          <button onClick={onClose} className="hover:text-slate-300">
            CLOSE INSPECTOR [ESC]
          </button>
        </div>
      </div>
    </div>
  );
}
