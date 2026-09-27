"use client";

import Link from "next/link";
import { motion } from "motion/react";
import {
  Compass,
  Sparkles,
  ShieldCheck,
  Copy,
  Send,
  Activity,
  ArrowRight,
  Database,
  Layers,
  AlertTriangle,
  GitBranch,
  Cpu,
  CheckCircle2,
  Waves
} from "lucide-react";
import { DemoBadge } from "@/components/ui/DemoBadge";

const STATS = [
  { label: "MONITORED SITES", value: "24", sub: "European urban basins", icon: Compass },
  { label: "EVIDENCE OBS", value: "1,420+", sub: "Sensor & citizen feeds", icon: Database },
  { label: "VERIFIED TRUST", value: "94.8%", sub: "Deterministic audit rate", icon: ShieldCheck },
  { label: "DISPATCHED MISSIONS", value: "38", sub: "Gaps prioritized", icon: Send },
];

const CAPABILITIES = [
  {
    title: "EVIDENCE PASSPORT X-RAY",
    tag: "INTEGRITY & TRUST",
    desc: "Evaluate spatial corroboration, temporal freshness, sensor schema compliance, and cross-observer concordance before acting on data.",
    href: "/trust",
    icon: ShieldCheck,
    color: "from-cyan-500/20 to-blue-600/20",
    border: "border-cyan-500/30",
    accent: "text-cyan-400"
  },
  {
    title: "ECOLOGICAL TWIN DISCOVERY",
    tag: "COMPARATIVE ANALYSIS",
    desc: "Match urban streams across 8 ecological dimensions (water chemistry, hydromorphology, biotics, EO signals) to find comparable restoration trajectories.",
    href: "/twins",
    icon: Copy,
    color: "from-blue-500/20 to-indigo-600/20",
    border: "border-blue-500/30",
    accent: "text-blue-400"
  },
  {
    title: "ORACLE & SKEPTIC CHALLENGE",
    tag: "GROUNDED REASONING",
    desc: "Query stream recovery hypotheses backed by strict evidence IDs. Toggle Skeptic mode to surface counter-evidence and identify knowledge gaps.",
    href: "/oracle",
    icon: Sparkles,
    color: "from-emerald-500/20 to-teal-600/20",
    border: "border-emerald-500/30",
    accent: "text-emerald-400"
  },
  {
    title: "MISSION CONTROL & DISPATCH",
    tag: "UNCERTAINTY REDUCTION",
    desc: "Algorithmic volunteer assignment that routes community scientists directly to critical knowledge gaps and uncorroborated anomaly locations.",
    href: "/missions",
    icon: Send,
    color: "from-violet-500/20 to-purple-600/20",
    border: "border-violet-500/30",
    accent: "text-violet-400"
  }
];

export default function Home() {
  return (
    <div className="relative overflow-hidden bg-[#06090e] text-slate-100">
      {/* Background ambient lighting */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[450px] bg-gradient-to-b from-cyan-950/20 via-blue-950/10 to-transparent blur-3xl pointer-events-none -z-10" />
      <div className="absolute top-1/4 right-0 w-[500px] h-[500px] bg-emerald-950/10 blur-[120px] pointer-events-none -z-10" />

      {/* Hero Section */}
      <section className="relative pt-16 pb-20 md:pt-24 md:pb-32 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="flex flex-col items-start gap-6 max-w-4xl">
          {/* Eyebrow badge */}
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="flex items-center gap-3 flex-wrap"
          >
            <DemoBadge />
            <span className="font-mono text-xs text-slate-400 tracking-wider flex items-center gap-1.5 bg-slate-900/80 px-3 py-1 rounded-full border border-slate-800">
              <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
              ECOSYSTEM GOVERNANCE NETWORK
            </span>
          </motion.div>

          {/* Main Title */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="space-y-4"
          >
            <h2 className="font-mono text-sm uppercase tracking-widest text-cyan-400 font-semibold">
              AQUARYS
            </h2>
            <h1 className="font-mono text-3xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-white uppercase leading-[1.1]">
              DON&apos;T JUST ASK WHAT THE RIVER SAYS.
              <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-blue-400">
                ASK WHETHER THE EVIDENCE DESERVES TO BE BELIEVED.
              </span>
            </h1>
          </motion.div>

          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-base sm:text-lg text-slate-300 max-w-2xl leading-relaxed"
          >
            Autonomous environmental intelligence, multi-dimensional stream fingerprinting, and evidence provenance for urban watershed restoration.
          </motion.p>

          {/* CTA Buttons */}
          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-wrap items-center gap-4 pt-4"
          >
            <Link
              href="/sites"
              className="inline-flex items-center gap-2.5 px-6 py-3 rounded-lg bg-cyan-500 text-slate-950 font-mono text-sm font-semibold hover:bg-cyan-400 transition-all shadow-[0_0_20px_rgba(6,182,212,0.3)] active:scale-95"
            >
              <Compass className="h-4 w-4" />
              <span>EXPLORE NETWORK</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <Link
              href="/sites/site-c1"
              className="inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-slate-900/90 border border-slate-700 text-slate-200 font-mono text-sm font-medium hover:border-cyan-500/50 hover:text-white transition-all active:scale-95"
            >
              <span>INSPECT SITE C1 (COIMBRA)</span>
            </Link>
          </motion.div>
        </div>

        {/* Live System Telemetry Strip */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mt-16 grid grid-cols-2 lg:grid-cols-4 gap-4 p-4 sm:p-6 rounded-xl bg-slate-950/60 border border-slate-800/80 backdrop-blur-sm shadow-xl"
        >
          {STATS.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <div key={i} className="flex flex-col gap-1 p-3 rounded-lg bg-slate-900/40 border border-slate-800/40">
                <div className="flex items-center justify-between text-slate-400 mb-1">
                  <span className="font-mono text-[11px] uppercase tracking-wider">{stat.label}</span>
                  <Icon className="h-4 w-4 text-cyan-400" />
                </div>
                <span className="font-mono text-2xl sm:text-3xl font-bold text-slate-100">{stat.value}</span>
                <span className="text-xs text-slate-400">{stat.sub}</span>
              </div>
            );
          })}
        </motion.div>
      </section>

      {/* Featured Stream Insight Snapshot */}
      <section className="py-16 border-t border-slate-800/60 bg-[#080d14]/60">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4">
            <div>
              <div className="flex items-center gap-2 font-mono text-xs text-cyan-400 tracking-wider mb-2">
                <Activity className="h-4 w-4 text-cyan-400" />
                <span>REAL-TIME STREAM INTELLIGENCE</span>
              </div>
              <h2 className="font-mono text-2xl sm:text-3xl font-bold text-slate-100">
                Active Benchmark: Rio Mondego (C1)
              </h2>
            </div>
            <Link
              href="/sites/site-c1"
              className="font-mono text-xs text-cyan-400 hover:text-cyan-300 flex items-center gap-1.5"
            >
              <span>View full telemetry</span>
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Stream Fingerprint Card */}
            <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs text-slate-400 uppercase tracking-wider">8-Axis Fingerprint</span>
                <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
                  91% COVERAGE
                </span>
              </div>
              <div className="space-y-2 font-mono text-xs">
                {[
                  { name: "Water Quality (DO/pH/Cond)", val: 78, status: "observed" },
                  { name: "Riparian Habitat Density", val: 64, status: "observed" },
                  { name: "Hydromorphological Integrity", val: 52, status: "derived" },
                  { name: "Benthic Macroinvertebrates", val: 81, status: "observed" },
                  { name: "Nutrient Load (NO3/PO4)", val: 45, status: "estimated" },
                ].map((item, idx) => (
                  <div key={idx} className="space-y-1">
                    <div className="flex justify-between text-[11px]">
                      <span className="text-slate-300">{item.name}</span>
                      <span className="text-cyan-400">{item.val}%</span>
                    </div>
                    <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 rounded-full"
                        style={{ width: `${item.val}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
              <div className="pt-2 flex items-center justify-between text-[11px] font-mono text-slate-400 border-t border-slate-800">
                <span>Missing: Heavy Metal Ion Assay</span>
                <span className="text-amber-400">GAP DETECTED</span>
              </div>
            </div>

            {/* Evidence Passport Verification */}
            <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs text-slate-400 uppercase tracking-wider">Evidence Passport</span>
                <span className="text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-800/40">
                  TRUST 94.2%
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                Deterministic validation confirms spatial concordance with Copernicus EO telemetry and citizen corroborated pH metrics.
              </p>
              <div className="grid grid-cols-2 gap-2 font-mono text-xs">
                <div className="p-2.5 rounded bg-slate-950/60 border border-slate-800/60">
                  <div className="text-[10px] text-slate-400">SPATIAL ACCURACY</div>
                  <div className="text-sm font-bold text-emerald-400">98.1% (±2.4m)</div>
                </div>
                <div className="p-2.5 rounded bg-slate-950/60 border border-slate-800/60">
                  <div className="text-[10px] text-slate-400">OBSERVER OVERLAP</div>
                  <div className="text-sm font-bold text-cyan-400">3 Observers</div>
                </div>
              </div>
              <div className="p-2.5 rounded bg-cyan-950/20 border border-cyan-900/30 flex items-center gap-2 text-xs font-mono text-cyan-300">
                <CheckCircle2 className="h-4 w-4 text-cyan-400 shrink-0" />
                <span>Zero fabrication anomalies detected in batch #081.</span>
              </div>
            </div>

            {/* Top Twin Match */}
            <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 space-y-4 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs text-slate-400 uppercase tracking-wider">Top Twin Candidate</span>
                  <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
                    92% SIMILARITY
                  </span>
                </div>
                <h3 className="font-mono text-base font-bold text-slate-100">G7 · Ghent (Leie Canal Basin)</h3>
                <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                  Comparable substrate porosity and seasonal runoff dynamics. Successfully completed 2024 willow-shading intervention with +34% DO recovery.
                </p>
              </div>
              <Link
                href="/twins"
                className="w-full py-2.5 px-4 rounded bg-slate-800 hover:bg-slate-700 text-center font-mono text-xs text-slate-200 transition-colors flex items-center justify-center gap-2"
              >
                <span>RUN TWIN COMPARISON</span>
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 4 Core Pillars Grid */}
      <section className="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16 space-y-3">
          <span className="font-mono text-xs uppercase tracking-widest text-cyan-400">
            INTELLIGENCE ARCHITECTURE
          </span>
          <h2 className="font-mono text-2xl sm:text-3xl lg:text-4xl font-bold text-white">
            Engineered for Environmental Evidence Integrity
          </h2>
          <p className="text-sm text-slate-400">
            Four interconnected modules providing verifiable observation ingestion, comparative ecological reasoning, and targeted mission dispatch.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {CAPABILITIES.map((cap, i) => {
            const Icon = cap.icon;
            return (
              <motion.div
                key={i}
                whileHover={{ y: -3 }}
                transition={{ duration: 0.2 }}
                className={`group p-6 sm:p-8 rounded-xl bg-slate-900/50 border ${cap.border} backdrop-blur-sm relative overflow-hidden flex flex-col justify-between`}
              >
                <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${cap.color} rounded-bl-full pointer-events-none opacity-50 group-hover:opacity-100 transition-opacity`} />
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <div className={`p-2.5 rounded-lg bg-slate-950/80 border border-slate-800 ${cap.accent}`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <span className="font-mono text-[10px] tracking-wider uppercase text-slate-400">
                      {cap.tag}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-mono text-lg font-bold text-slate-100 group-hover:text-cyan-300 transition-colors">
                      {cap.title}
                    </h3>
                    <p className="text-xs sm:text-sm text-slate-400 mt-2 leading-relaxed">
                      {cap.desc}
                    </p>
                  </div>
                </div>

                <div className="pt-6 mt-6 border-t border-slate-800/80 flex items-center justify-between">
                  <Link
                    href={cap.href}
                    className={`font-mono text-xs font-semibold ${cap.accent} flex items-center gap-1.5 group-hover:translate-x-1 transition-transform`}
                  >
                    <span>LAUNCH INTERFACE</span>
                    <ArrowRight className="h-3.5 w-3.5" />
                  </Link>
                </div>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* Mission & Governance Callout */}
      <section className="py-16 border-t border-slate-800 bg-[#04070b]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col lg:flex-row items-center justify-between gap-8">
          <div className="space-y-3 max-w-2xl">
            <span className="font-mono text-xs uppercase tracking-widest text-emerald-400">
              OPEN ENVIRONMENTAL OBSERVATION INTEROPERABILITY
            </span>
            <h2 className="font-mono text-2xl sm:text-3xl font-bold text-white">
              Deterministic FHIR v4 Observation Bundles
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
              Every AQUARYS insight produces auditable HL7 FHIR RiskAssessment and Observation bundles, ensuring cross-agency compliance with European Water Framework Directive (WFD) guidelines.
            </p>
          </div>

          <div className="flex flex-wrap gap-4 font-mono text-xs">
            <Link
              href="/missions"
              className="px-6 py-3 rounded-lg bg-emerald-500 text-slate-950 font-semibold hover:bg-emerald-400 transition-colors flex items-center gap-2"
            >
              <Send className="h-4 w-4" />
              <span>DISPATCH VOLUNTEER MISSION</span>
            </Link>
            <Link
              href="/evidence/claim-001"
              className="px-5 py-3 rounded-lg bg-slate-900 border border-slate-800 text-slate-200 hover:border-slate-700 transition-colors flex items-center gap-2"
            >
              <GitBranch className="h-4 w-4 text-cyan-400" />
              <span>INSPECT PROVENANCE GRAPH</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
