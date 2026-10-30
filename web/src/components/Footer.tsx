import Link from "next/link";
import { MessageSquare, Shield } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white text-slate-600 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
        <div className="space-y-4 md:col-span-1">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white">
              <MessageSquare className="w-4 h-4 fill-white" />
            </div>
            <span className="font-bold text-lg text-slate-900">WhatsPulse SaaS</span>
          </div>
          <p className="text-xs text-slate-500 leading-relaxed">
            The next-generation WhatsApp marketing, notice broadcasting, and student outreach automation platform built with multi-variant anti-restriction safety.
          </p>
          <div className="flex items-center gap-2 text-xs text-emerald-700 font-medium">
            <Shield className="w-3.5 h-3.5" />
            <span>Anti-Restriction Algorithm v2.4</span>
          </div>
        </div>

        <div>
          <h4 className="text-sm font-bold text-slate-900 mb-3 tracking-wide">Product</h4>
          <ul className="space-y-2 text-xs">
            <li><Link href="#features" className="hover:text-emerald-600 transition-colors">Anti-Ban Message Studio</Link></li>
            <li><Link href="#simulator" className="hover:text-emerald-600 transition-colors">Sequential Spintax Engine</Link></li>
            <li><Link href="#calculator" className="hover:text-emerald-600 transition-colors">Meta API Savings Calculator</Link></li>
            <li><Link href="/app/connect" className="hover:text-emerald-600 transition-colors">Web QR Code Engine</Link></li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm font-bold text-slate-900 mb-3 tracking-wide">Solutions</h4>
          <ul className="space-y-2 text-xs">
            <li><span className="text-slate-600">Coaching Centers &amp; Academies</span></li>
            <li><span className="text-slate-600">Colleges &amp; Schools</span></li>
            <li><span className="text-slate-600">E-commerce Customer Updates</span></li>
            <li><span className="text-slate-600">Service Appointment Alerts</span></li>
          </ul>
        </div>

        <div>
          <h4 className="text-sm font-bold text-slate-900 mb-3 tracking-wide">Legal &amp; Policy</h4>
          <ul className="space-y-2 text-xs">
            <li><span className="text-slate-600 hover:text-slate-900 cursor-pointer">Terms of Service</span></li>
            <li><span className="text-slate-600 hover:text-slate-900 cursor-pointer">Privacy Policy</span></li>
            <li><span className="text-slate-600 hover:text-slate-900 cursor-pointer">WhatsApp Compliance Guidelines</span></li>
            <li><span className="text-slate-600 hover:text-slate-900 cursor-pointer">Contact Support</span></li>
          </ul>
          <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-200 text-[11px] text-slate-500">
            Not affiliated with Meta or WhatsApp Inc. Uses user-controlled local session protocols.
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto mt-8 pt-8 border-t border-slate-200 text-center text-xs text-slate-400">
        © 2026 WhatsPulse SaaS. All rights reserved. Built for education &amp; business communicators.
      </div>
    </footer>
  );
}
