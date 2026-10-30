"use client";

import Link from "next/link";
import { useState } from "react";
import { Navbar } from "../components/Navbar";
import { Footer } from "../components/Footer";
import { AntiBanSimulator } from "../components/AntiBanSimulator";
import { RoiCalculator } from "../components/RoiCalculator";
import {
  Shield,
  Zap,
  Users,
  Layers,
  ArrowRight,
  CheckCircle2,
  Sparkles,
  Smartphone,
  BarChart3,
  Check,
  ChevronDown,
  MessageSquare
} from "lucide-react";

export default function LandingPage() {
  const [billingCycle, setBillingCycle] = useState<"monthly" | "annual">("monthly");
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const discountMultiplier = billingCycle === "annual" ? 0.8 : 1;

  const faqs = [
    {
      q: "How does the Anti-Restriction Matrix protect my WhatsApp account?",
      a: "When you blast the same text message to dozens of recipients in a short time, WhatsApp's automated spam algorithms flag your account. WhatsPulse rotates 3 to 5 completely different SMS designs in sequential round-robin order, plus randomized Spintax variants. To WhatsApp, every message looks uniquely composed, drastically lowering restriction risks."
    },
    {
      q: "What happens if a student's number does not have a WhatsApp account?",
      a: "Our system automatically detects WhatsApp's 'Phone number shared via url is invalid' popup, auto-dismisses the modal with zero delay, marks the number as 'Skipped' in your dashboard, and instantly proceeds to the next student. Your campaign never stalls or counts it as a delivery failure."
    },
    {
      q: "Do I need Meta Cloud API approval or credit card verification?",
      a: "No! WhatsPulse operates directly with your phone number via a quick Web QR Code connection. You don't need a Facebook Developer account, business manager verification, or template approval from Meta."
    },
    {
      q: "Can I import students from Excel and CSV files?",
      a: "Yes. You can drag and drop your `.xlsx` or `.csv` files. The system auto-cleans country codes, validates phone formats, strips duplicates, and keeps leading zeros intact."
    },
    {
      q: "Can multiple team members manage campaigns?",
      a: "Yes, on our Pro and Agency plans, you can invite team coordinators and coaching managers to compose messages, upload batches, and monitor live progress."
    }
  ];

  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 selection:bg-emerald-500 selection:text-slate-950">
      <Navbar />

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto overflow-hidden">
        {/* Glow ambient background */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-emerald-500/10 rounded-full blur-[140px] pointer-events-none" />

        <div className="text-center max-w-4xl mx-auto space-y-6 relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold shadow-inner">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span>Version 2.4 Live &bull; Multi-SMS Anti-Restriction Engine</span>
          </div>

          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.1]">
            WhatsApp Bulk Messaging <br className="hidden sm:inline" />
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
              Without Spam Restrictions
            </span>
          </h1>

          <p className="text-slate-400 text-base sm:text-xl max-w-2xl mx-auto leading-relaxed">
            The all-in-one SaaS platform for academies, coaching centers, and businesses. Rotate 3–5 SMS designs sequentially, auto-skip invalid numbers, and broadcast with zero per-message Meta fees.
          </p>

          {/* Action CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <Link
              href="/app"
              className="w-full sm:w-auto flex items-center justify-center gap-2.5 px-8 py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold text-base shadow-xl shadow-emerald-500/25 transition-all hover:scale-[1.02] active:scale-[0.98]"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="#simulator"
              className="w-full sm:w-auto flex items-center justify-center gap-2 px-7 py-4 rounded-xl bg-slate-900/90 hover:bg-slate-850 text-slate-200 font-semibold text-base border border-slate-800 transition-all hover:border-slate-700"
            >
              <span>Try Anti-Ban Simulator</span>
            </Link>
          </div>

          {/* Social Proof Pills */}
          <div className="pt-8 flex flex-wrap items-center justify-center gap-6 sm:gap-10 text-xs font-medium text-slate-400">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Zero Meta API Markup</span>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="w-4 h-4 text-emerald-400" />
              <span>Multi-Design Sequential Rotation</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="w-4 h-4 text-emerald-400" />
              <span>Auto-Skip Non-WhatsApp Numbers</span>
            </div>
          </div>
        </div>

        {/* Hero App Mockup Preview */}
        <div className="mt-16 max-w-5xl mx-auto rounded-2xl glass-panel p-2 sm:p-4 border border-slate-800 shadow-2xl relative">
          <div className="bg-slate-950 rounded-xl overflow-hidden border border-slate-850 p-4 sm:p-6 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-slate-850 text-xs">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full bg-red-500/80 inline-block" />
                <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block" />
                <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block" />
                <span className="ml-2 font-mono text-slate-400">WhatsPulse Campaign Dispatcher</span>
              </div>
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[11px] font-semibold border border-emerald-500/20">
                ● Live Dispatching &bull; 17 / 17 Students
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-slate-500 block mb-1">Rotating Variations</span>
                <span className="text-white font-bold text-sm">3 SMS Designs Active</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-slate-500 block mb-1">Queue Status</span>
                <span className="text-emerald-400 font-bold text-sm">15 Delivered &bull; 2 Auto-Skipped</span>
              </div>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-slate-500 block mb-1">Anti-Restriction Safety</span>
                <span className="text-teal-300 font-bold text-sm">Active (Round Robin)</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Simulator Section */}
      <AntiBanSimulator />

      {/* Core Features Grid */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Built For Scale</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Everything You Need to Run High-Converting Campaigns
          </h2>
          <p className="mt-3 text-slate-400 text-sm sm:text-base">
            Engineered specifically to solve the biggest headaches of WhatsApp marketing: spam detection, invalid numbers, and high Meta conversation costs.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center border border-emerald-500/20">
              <Shield className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Multi-SMS Variant Rotation</h3>
            <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">
              Create 3, 4, or 5 SMS variants. Student #1 gets design 1, Student #2 gets design 2, Student #3 gets design 3. No two consecutive messages are ever identical.
            </p>
          </div>

          {/* Card 2 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4">
            <div className="w-10 h-10 rounded-xl bg-teal-500/10 text-teal-400 flex items-center justify-center border border-teal-500/20">
              <Zap className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Auto-Skip Invalid Numbers</h3>
            <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">
              If a number has no WhatsApp account, the system catches the modal, dismisses it, marks the recipient as skipped, and instantly moves to the next student.
            </p>
          </div>

          {/* Card 3 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4">
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center border border-cyan-500/20">
              <Smartphone className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Instant QR Code Connection</h3>
            <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">
              Scan once directly from your phone&apos;s WhatsApp (Linked Devices). No complicated Facebook Business Manager, no API tokens, and no setup fees.
            </p>
          </div>

          {/* Card 4 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4">
            <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center border border-amber-500/20">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Spintax Dynamic Parser</h3>
            <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">
              Use &#123;Hello|Hi|Dear&#125; syntax to dynamically spin greetings, sentences, and sign-offs for unlimited unique message permutations.
            </p>
          </div>

          {/* Card 5 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4">
            <div className="w-10 h-10 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center border border-indigo-500/20">
              <Users className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Excel & CSV Contact CRM</h3>
            <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">
              Upload class rosters, customer spreadsheets, or applicant lists. Automatic country code normalization (+880, +1, etc.) and duplicate suppression.
            </p>
          </div>

          {/* Card 6 */}
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition-all space-y-4">
            <div className="w-10 h-10 rounded-xl bg-rose-500/10 text-rose-400 flex items-center justify-center border border-rose-500/20">
              <BarChart3 className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Audit Reports & Export</h3>
            <p className="text-slate-400 text-xs sm:text-sm leading-relaxed">
              Export detailed Excel/CSV logs with exact delivery timestamps, which variant was delivered to which student, and non-WhatsApp lists.
            </p>
          </div>
        </div>
      </section>

      {/* ROI Calculator Section */}
      <RoiCalculator />

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-4">
            <span>Simple, Flat Pricing</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Start Broadcasting with Zero Per-Message Fees
          </h2>
          <p className="mt-3 text-slate-400 text-sm sm:text-base">
            Choose the plan that fits your academy or business. Upgrade, downgrade, or cancel at any time.
          </p>

          {/* Monthly / Annual toggle */}
          <div className="mt-8 inline-flex items-center gap-2 p-1 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold">
            <button
              onClick={() => setBillingCycle("monthly")}
              className={`px-4 py-2 rounded-lg transition-all ${
                billingCycle === "monthly" ? "bg-emerald-500 text-slate-950 font-bold shadow" : "text-slate-400 hover:text-white"
              }`}
            >
              Monthly Billing
            </button>
            <button
              onClick={() => setBillingCycle("annual")}
              className={`px-4 py-2 rounded-lg flex items-center gap-1.5 transition-all ${
                billingCycle === "annual" ? "bg-emerald-500 text-slate-950 font-bold shadow" : "text-slate-400 hover:text-white"
              }`}
            >
              <span>Annual Billing</span>
              <span className="text-[10px] uppercase font-extrabold px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300">
                20% OFF
              </span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-stretch">
          {/* Starter Plan */}
          <div className="glass-panel rounded-2xl p-8 border border-slate-800 flex flex-col justify-between hover:border-slate-700 transition-all">
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-bold text-white">Starter</h3>
                <p className="text-xs text-slate-400 mt-1">For single tutors and small coaching batches</p>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-extrabold text-white font-mono">
                  ${Math.round(19 * discountMultiplier)}
                </span>
                <span className="text-xs text-slate-400">/ month</span>
              </div>
              <ul className="space-y-3 text-xs text-slate-300">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> 1 WhatsApp Number</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> Up to 3,000 Messages / mo</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> 3-Variant Anti-Restriction Studio</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> Auto-Skip Non-WhatsApp Numbers</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> CSV & Excel Contact Import</li>
              </ul>
            </div>
            <Link
              href="/app"
              className="mt-8 w-full block text-center py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs border border-slate-800 transition-all"
            >
              Start Free Trial
            </Link>
          </div>

          {/* Pro Plan (Featured) */}
          <div className="glass-panel rounded-2xl p-8 border-2 border-emerald-500 shadow-2xl relative flex flex-col justify-between scale-[1.02] bg-slate-950/90">
            <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 px-3 py-1 rounded-full bg-emerald-500 text-slate-950 text-xs font-bold uppercase tracking-wide">
              Most Popular
            </div>
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-bold text-white">Pro Academy</h3>
                <p className="text-xs text-slate-400 mt-1">For large coaching centers & high-volume schools</p>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-extrabold text-emerald-400 font-mono">
                  ${Math.round(49 * discountMultiplier)}
                </span>
                <span className="text-xs text-slate-400">/ month</span>
              </div>
              <ul className="space-y-3 text-xs text-slate-200">
                <li className="flex items-center gap-2 font-medium"><Check className="w-4 h-4 text-emerald-400" /> 3 WhatsApp Numbers Connected</li>
                <li className="flex items-center gap-2 font-medium"><Check className="w-4 h-4 text-emerald-400" /> Up to 25,000 Messages / mo</li>
                <li className="flex items-center gap-2 font-medium"><Check className="w-4 h-4 text-emerald-400" /> Unlimited SMS Variations & Spintax</li>
                <li className="flex items-center gap-2 font-medium"><Check className="w-4 h-4 text-emerald-400" /> Priority Fast-Track Dispatch Engine</li>
                <li className="flex items-center gap-2 font-medium"><Check className="w-4 h-4 text-emerald-400" /> Real-time Delivery Audit Reports</li>
                <li className="flex items-center gap-2 font-medium"><Check className="w-4 h-4 text-emerald-400" /> Priority WhatsApp & Email Support</li>
              </ul>
            </div>
            <Link
              href="/app"
              className="mt-8 w-full block text-center py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/25 transition-all"
            >
              Get Started with Pro
            </Link>
          </div>

          {/* Agency Plan */}
          <div className="glass-panel rounded-2xl p-8 border border-slate-800 flex flex-col justify-between hover:border-slate-700 transition-all">
            <div className="space-y-6">
              <div>
                <h3 className="text-xl font-bold text-white">Enterprise / Agency</h3>
                <p className="text-xs text-slate-400 mt-1">For educational networks & marketing agencies</p>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-extrabold text-white font-mono">
                  ${Math.round(99 * discountMultiplier)}
                </span>
                <span className="text-xs text-slate-400">/ month</span>
              </div>
              <ul className="space-y-3 text-xs text-slate-300">
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> Unlimited WhatsApp Numbers</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> Up to 100,000 Messages / mo</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> Multi-User Team Roles & Permissions</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> Custom Webhook & REST API Access</li>
                <li className="flex items-center gap-2"><Check className="w-4 h-4 text-emerald-400" /> Dedicated Account Manager & Training</li>
              </ul>
            </div>
            <Link
              href="/app"
              className="mt-8 w-full block text-center py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs border border-slate-800 transition-all"
            >
              Contact Sales
            </Link>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="py-20 px-4 sm:px-6 lg:px-8 max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-extrabold text-white tracking-tight">Frequently Asked Questions</h2>
          <p className="text-slate-400 text-sm mt-2">Clear answers to help you get started safely and quickly.</p>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, idx) => (
            <div
              key={idx}
              className="glass-panel rounded-xl border border-slate-800 overflow-hidden transition-all"
            >
              <button
                onClick={() => setOpenFaq(openFaq === idx ? null : idx)}
                className="w-full flex items-center justify-between p-5 text-left text-sm font-semibold text-white hover:text-emerald-400 transition-colors"
              >
                <span>{faq.q}</span>
                <ChevronDown className={`w-4 h-4 transition-transform ${openFaq === idx ? "rotate-180 text-emerald-400" : "text-slate-500"}`} />
              </button>
              {openFaq === idx && (
                <div className="px-5 pb-5 text-xs text-slate-300 leading-relaxed border-t border-slate-850 pt-3">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* Bottom CTA Banner */}
      <section className="py-16 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
        <div className="rounded-3xl p-8 sm:p-12 bg-gradient-to-r from-emerald-950/60 via-slate-950 to-teal-950/60 border border-emerald-500/30 text-center space-y-6 relative overflow-hidden">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
            Ready to Scale Your WhatsApp Broadcasts Safely?
          </h2>
          <p className="text-slate-300 text-sm max-w-xl mx-auto">
            Join hundreds of educators and businesses broadcasting with high inbox deliverability and zero surprise bills.
          </p>
          <div className="pt-2">
            <Link
              href="/app"
              className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-base shadow-xl shadow-emerald-500/20 transition-all hover:scale-[1.02]"
            >
              <span>Launch Web Application</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
