"use client";

import Link from "next/link";
import { MessageSquare, ShieldCheck, Zap, ArrowRight, Menu, X } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-slate-950 shadow-lg shadow-emerald-500/20">
              <MessageSquare className="w-5 h-5 fill-slate-950 text-slate-950" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-lg tracking-tight text-white flex items-center gap-1.5">
                WhatsPulse <span className="text-[10px] uppercase tracking-wider font-semibold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">SaaS</span>
              </span>
            </div>
          </Link>

          {/* Desktop Navigation Links */}
          <div className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
            <Link href="#simulator" className="hover:text-emerald-400 transition-colors">Anti-Ban Simulator</Link>
            <Link href="#features" className="hover:text-emerald-400 transition-colors">Features</Link>
            <Link href="#calculator" className="hover:text-emerald-400 transition-colors">ROI Savings</Link>
            <Link href="#pricing" className="hover:text-emerald-400 transition-colors">Pricing</Link>
            <Link href="#faq" className="hover:text-emerald-400 transition-colors">FAQ</Link>
          </div>

          {/* Right Action Buttons */}
          <div className="hidden md:flex items-center space-x-4">
            <Link
              href="/app"
              className="text-xs uppercase tracking-wider font-semibold text-slate-400 hover:text-white px-3 py-2 transition-colors"
            >
              Sign In
            </Link>
            <Link
              href="/app"
              className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-sm shadow-md shadow-emerald-500/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              <span>Launch App</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-slate-400 hover:text-white p-2"
              aria-label="Toggle menu"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden px-4 pt-2 pb-6 space-y-3 bg-slate-950/95 border-b border-slate-800">
          <Link
            href="#simulator"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-slate-300 hover:text-emerald-400 py-2 text-base font-medium"
          >
            Anti-Ban Simulator
          </Link>
          <Link
            href="#features"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-slate-300 hover:text-emerald-400 py-2 text-base font-medium"
          >
            Features
          </Link>
          <Link
            href="#pricing"
            onClick={() => setMobileMenuOpen(false)}
            className="block text-slate-300 hover:text-emerald-400 py-2 text-base font-medium"
          >
            Pricing
          </Link>
          <Link
            href="/app"
            onClick={() => setMobileMenuOpen(false)}
            className="w-full flex items-center justify-center gap-2 py-3 rounded-lg bg-emerald-500 text-slate-950 font-bold text-center"
          >
            Launch Web App <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      )}
    </nav>
  );
}
