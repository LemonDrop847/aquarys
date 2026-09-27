"use client";

import { motion } from "motion/react";

interface StreamFingerprintProps {
  siteId: string;
}

export function StreamFingerprint({ siteId }: StreamFingerprintProps) {
  const dimensions = [
    { name: "Water", value: 78, status: "observed" },
    { name: "Habitat", value: 64, status: "observed" },
    { name: "Vegetation", value: 82, status: "derived" },
    { name: "Hydromorphology", value: 52, status: "observed" },
    { name: "Biotics", value: 81, status: "observed" },
    { name: "Nutrients", value: 45, status: "estimated" },
    { name: "EO", value: 94, status: "observed" },
    { name: "Citizen", value: 0, status: "missing" }
  ];

  return (
    <div className="space-y-3">
      {dimensions.map((dim, i) => (
        <div key={dim.name} className="space-y-1 relative">
          <div className="flex justify-between text-[11px] font-mono">
            <span className="text-slate-300">{dim.name}</span>
            <span className={dim.status === "missing" ? "text-amber-500" : "text-cyan-400"}>
              {dim.status === "missing" ? "NO DATA" : `${dim.value}%`}
            </span>
          </div>
          <div className={`w-full h-1.5 rounded-full overflow-hidden ${dim.status === "missing" ? "bg-amber-950/30 border border-dashed border-amber-900/50" : "bg-slate-800"}`}>
            {dim.status !== "missing" && (
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${dim.value}%` }}
                transition={{ duration: 0.8, delay: i * 0.1 }}
                className="h-full bg-gradient-to-r from-cyan-500 to-emerald-500 rounded-full"
              />
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
