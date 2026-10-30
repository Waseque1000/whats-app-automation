import Link from "next/link";
import { MessageSquare, Shield, CheckCircle2 } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-slate-850 bg-slate-950/80 text-slate-400 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="space-y-4 md:col-span-1">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center text-slate-950">
              <MessageSquare className="w-4 h-4 fill-slate-950" />
            </div>
            <span className="font-bold text-lg text-white">WhatsPulse SaaS</span>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            The next-generation WhatsApp marketing, notice broadcasting, and student outreach automation platform built with multi-variant anti-restriction safety.
          </p>
          <div className="flex items-center gap-2 text-xs text-emerald-400">
            <Shield className="w-3.5 h-3.5" />
            <span>Anti-Restriction Algorithm v2.4</span>
          </div>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-white mb-3 tracking-wide">Product</h4>
          <ul className="space-y-2 text-xs">
            <li><Link href="#features" className="hover:text-emerald-400 transition-colors">Anti-Ban Message Studio</Link></li>
            <li><Link href="#simulator" className="hover:text-emerald-400 transition-colors">Sequential Spintax Engine</Link></li>
            <li><Link href="#calculator" className="hover:text-emerald-400 transition-colors">Meta API Savings Calculator</Link></li>
            <li><Link href="/app/connect" className="hover:text-emerald-400 transition-colors">Web QR Code Engine</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-white mb-3 tracking-wide">Solutions</h4>
          <ul className="space-y-2 text-xs">
            <li><span className="text-slate-300">Coaching Centers & Academies</span></li>
            <li><span className="text-slate-300">Colleges & Schools</span></li>
            <li><span className="text-slate-300">E-commerce Customer Updates</span></li>
            <li><span className="text-slate-300">Service Appointment Alerts</span></li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm font-semibold text-white mb-3 tracking-wide">Legal & Policy</h4>
          <ul className="space-y-2 text-xs">
            <li><span className="text-slate-400 hover:text-white cursor-pointer">Terms of Service</span></li>
            <li><span className="text-slate-400 hover:text-white cursor-pointer">Privacy Policy</span></li>
            <li><span className="text-slate-400 hover:text-white cursor-pointer">WhatsApp Compliance Guidelines</span></li>
            <li><span className="text-slate-400 hover:text-white cursor-pointer">Contact Support</span></li>
          </ul>
          <div className="mt-4 p-3 rounded-lg bg-slate-900 border border-slate-800 text-[11px] text-slate-400">
            Not affiliated with Meta or WhatsApp Inc. Uses user-controlled local session protocols.
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto mt-8 pt-8 border-t border-slate-900 text-center text-xs text-slate-500">
        © 2026 WhatsPulse SaaS. All rights reserved. Built for education & business communicators.
      </div>
    </footer>
  );
}
