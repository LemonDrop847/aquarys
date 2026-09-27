"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { DemoBadge } from "@/components/ui/DemoBadge";
import {
  Compass,
  ShieldCheck,
  Copy,
  Sparkles,
  Send,
  Menu,
  X,
  Layers
} from "lucide-react";

const NAV_ITEMS = [
  { label: "NETWORK", href: "/sites", icon: Compass },
  { label: "ORACLE", href: "/oracle", icon: Sparkles },
  { label: "TRUST", href: "/trust", icon: ShieldCheck },
  { label: "TWINS", href: "/twins", icon: Copy },
  { label: "MISSIONS", href: "/missions", icon: Send },
];

export function Navbar() {
  const pathname = usePathname();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-slate-800/80 bg-[#06090e]/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <Link href="/" className="flex items-center gap-3 group">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/40 text-cyan-400 group-hover:border-cyan-400 transition-colors">
              <Layers className="h-5 w-5" />
            </div>
            <div className="flex flex-col">
              <span className="font-mono text-base font-bold tracking-widest text-slate-100 group-hover:text-cyan-400 transition-colors">
                AQUARYS
              </span>
              <span className="text-[10px] font-mono text-slate-400 tracking-wider">
                RIVER INTELLIGENCE
              </span>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1">
            {NAV_ITEMS.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-md text-xs font-mono tracking-wider transition-all ${
                    isActive
                      ? "bg-cyan-950/60 text-cyan-300 border border-cyan-500/40 shadow-[0_0_12px_rgba(6,182,212,0.15)]"
                      : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/60"
                  }`}
                >
                  <Icon className={`h-3.5 w-3.5 ${isActive ? "text-cyan-400" : "text-slate-400"}`} />
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="hidden sm:flex items-center gap-4">
          <DemoBadge />
          <Link
            href="/sites/site-c1"
            className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-slate-900 border border-slate-800 text-xs font-mono text-slate-300 hover:border-slate-700 hover:text-white transition-all"
          >
            <span className="h-2 w-2 rounded-full bg-emerald-400"></span>
            <span>C1 · COIMBRA</span>
          </Link>
        </div>

        {/* Mobile Hamburger */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="md:hidden p-2 rounded-md text-slate-400 hover:text-white hover:bg-slate-800"
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-800 bg-[#06090e] px-4 py-4 space-y-2">
          <div className="pb-2 flex items-center justify-between border-b border-slate-800/60">
            <DemoBadge />
            <Link
              href="/sites/site-c1"
              onClick={() => setMobileMenuOpen(false)}
              className="text-xs font-mono text-cyan-400"
            >
              ACTIVE: C1 COIMBRA
            </Link>
          </div>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname.startsWith(`${item.href}/`);
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileMenuOpen(false)}
                className={`flex items-center gap-3 px-3 py-2 rounded-md text-sm font-mono ${
                  isActive
                    ? "bg-cyan-950/60 text-cyan-300 border border-cyan-500/40"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                }`}
              >
                <Icon className="h-4 w-4 text-cyan-400" />
                {item.label}
              </Link>
            );
          })}
        </div>
      )}
    </header>
  );
}
