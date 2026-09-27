"use client";

import { useState } from "react";
import { FHIRBundle } from "@/lib/types";
import { Copy, Download, Check, X, ShieldAlert, Code2 } from "lucide-react";

interface FHIRExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  bundle: FHIRBundle | null;
  isLoading?: boolean;
}

export function FHIRExportModal({
  isOpen,
  onClose,
  bundle,
  isLoading
}: FHIRExportModalProps) {
  const [copied, setCopied] = useState(false);

  if (!isOpen) return null;

  const jsonString = bundle ? JSON.stringify(bundle, null, 2) : "{}";

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
    a.download = `aquarys-fhir-bundle-${bundle?.id || "export"}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="w-full max-w-3xl rounded-xl bg-slate-900 border border-slate-800 shadow-2xl overflow-hidden font-mono flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center gap-2">
            <Code2 className="h-4 w-4 text-emerald-400" />
            <h3 className="text-xs uppercase tracking-wider font-bold text-slate-100">
              HL7 FHIR v4 EVIDENCE BUNDLE EXPORT
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 flex-1 overflow-y-auto space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 pb-2 border-b border-slate-800/80">
            <div>
              <span className="text-slate-500">RESOURCE TYPE:</span>{" "}
              <span className="text-cyan-400 font-bold">{bundle?.resourceType || "Bundle"}</span>
            </div>
            <div>
              <span className="text-slate-500">ENTRIES:</span>{" "}
              <span className="text-emerald-400 font-bold">{bundle?.entry?.length || 0} RESOURCES</span>
            </div>
          </div>

          {isLoading ? (
            <div className="py-20 flex flex-col items-center justify-center gap-3">
              <div className="w-6 h-6 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin" />
              <div className="text-xs text-slate-400">Compiling FHIR Standard JSON Schema...</div>
            </div>
          ) : (
            <pre className="p-4 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-300 overflow-x-auto leading-relaxed max-h-[50vh]">
              {jsonString}
            </pre>
          )}
        </div>

        {/* Footer */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between gap-3">
          <div className="text-[10px] text-slate-500 flex items-center gap-1.5">
            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
            COMPLIANT WITH HL7 FHIR v4.0.1
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs border border-slate-700 transition-colors"
            >
              {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
              <span>{copied ? "COPIED" : "COPY JSON"}</span>
            </button>
            <button
              onClick={handleDownload}
              className="flex items-center gap-1.5 px-4 py-1.5 rounded bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-colors shadow-sm"
            >
              <Download className="h-3.5 w-3.5" />
              <span>DOWNLOAD BUNDLE</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
