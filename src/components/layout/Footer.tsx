import Link from "next/link";
import { ShieldCheck, Activity, Terminal } from "lucide-react";

export function Footer() {
  return (
    <footer className="w-full border-t border-slate-800/80 bg-[#04060a] text-slate-400 py-10 mt-auto">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <span className="font-mono text-sm font-bold tracking-widest text-slate-200">
                AQUARYS
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800/40">
                v1.0.4-PROD
              </span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Autonomous environmental intelligence and evidence verification network for urban streams and watershed governance.
            </p>
          </div>

          <div>
            <h4 className="font-mono text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Intelligence Core
            </h4>
            <ul className="space-y-2 text-xs font-mono">
              <li>
                <Link href="/oracle" className="hover:text-cyan-400 transition-colors">
                  Oracle Investigations
                </Link>
              </li>
              <li>
                <Link href="/trust" className="hover:text-cyan-400 transition-colors">
                  Evidence Passport X-RAY
                </Link>
              </li>
              <li>
                <Link href="/twins" className="hover:text-cyan-400 transition-colors">
                  Ecological Twin Discovery
                </Link>
              </li>
              <li>
                <Link href="/missions" className="hover:text-cyan-400 transition-colors">
                  Mission Control & Dispatch
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-mono text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Network Monitoring
            </h4>
            <ul className="space-y-2 text-xs font-mono">
              <li>
                <Link href="/sites" className="hover:text-cyan-400 transition-colors">
                  European Stream Nodes
                </Link>
              </li>
              <li>
                <Link href="/sites/site-c1" className="hover:text-cyan-400 transition-colors">
                  Coimbra River (Mondego)
                </Link>
              </li>
              <li>
                <Link href="/evidence/claim-001" className="hover:text-cyan-400 transition-colors">
                  Provenance Graph Explorer
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-mono text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">
              Standards & Integrity
            </h4>
            <div className="space-y-2 text-xs text-slate-400">
              <div className="flex items-center gap-1.5 text-slate-300">
                <ShieldCheck className="h-4 w-4 text-emerald-400" />
                <span>HL7 FHIR Interoperable</span>
              </div>
              <div className="flex items-center gap-1.5 text-slate-300">
                <Activity className="h-4 w-4 text-cyan-400" />
                <span>Deterministic Evidence Engine</span>
              </div>
              <p className="text-[11px] text-slate-400 pt-1">
                Grounded empirical correlation without unverified hallucination.
              </p>
            </div>
          </div>
        </div>

        <div className="border-t border-slate-900 pt-6 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-mono text-slate-400">
          <div>
            © {new Date().getFullYear()} AQUARYS SCIENTIFIC. ALL EVIDENCE TRACKED UNDER VERIFIABLE AUDIT PROVENANCE.
          </div>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
              NODE CLUSTER HEALTHY
            </span>
            <span>REST API / FHIR v4</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
