"use client";

import { useState } from "react";
import { DollarSign, Check, TrendingUp, Sparkles } from "lucide-react";

export function RoiCalculator() {
  const [messagesPerMonth, setMessagesPerMonth] = useState(15000);
  const [currency, setCurrency] = useState<"USD" | "BDT">("USD");

  const metaCostPerMsg = 0.025; // average Meta API conversation fee
  const metaCostUsd = messagesPerMonth * metaCostPerMsg;
  const whatsPulseCostUsd = 49; // Flat Pro Plan
  const savingsUsd = Math.max(0, metaCostUsd - whatsPulseCostUsd);

  const exchangeRate = 120; // 1 USD = 120 BDT
  const metaCostDisplay = currency === "USD" ? `$${Math.round(metaCostUsd)}` : `৳${(Math.round(metaCostUsd * exchangeRate)).toLocaleString()}`;
  const whatsPulseCostDisplay = currency === "USD" ? `$${whatsPulseCostUsd}` : `৳${(whatsPulseCostUsd * exchangeRate).toLocaleString()}`;
  const savingsDisplay = currency === "USD" ? `$${Math.round(savingsUsd)}` : `৳${(Math.round(savingsUsd * exchangeRate)).toLocaleString()}`;
  const percentageSaved = Math.round((savingsUsd / Math.max(metaCostUsd, 1)) * 100);

  return (
    <section id="calculator" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="glass-panel rounded-3xl p-8 sm:p-12 border border-slate-800 shadow-2xl relative overflow-hidden">
        {/* Glow backdrop */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10">
          <div className="lg:col-span-6 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>Instant Cost Comparison</span>
            </div>

            <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
              Calculate Your <span className="text-emerald-400">Monthly Savings</span> vs Meta API
            </h2>

            <p className="text-slate-400 text-sm leading-relaxed">
              Meta charges for every single marketing conversation (~$0.025 - $0.035 each). With WhatsPulse, your team uses your own WhatsApp Web numbers with flat, predictable subscription pricing.
            </p>

            {/* Slider */}
            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-300">Monthly WhatsApp Messages:</span>
                <span className="text-lg font-bold text-emerald-400 font-mono">
                  {messagesPerMonth.toLocaleString()} messages
                </span>
              </div>
              <input
                type="range"
                min={2000}
                max={60000}
                step={1000}
                value={messagesPerMonth}
                onChange={(e) => setMessagesPerMonth(Number(e.target.value))}
                className="w-full accent-emerald-500 cursor-pointer h-2 bg-slate-800 rounded-lg"
              />
              <div className="flex justify-between text-[11px] text-slate-500">
                <span>2,000 / mo</span>
                <span>30,000 / mo</span>
                <span>60,000 / mo</span>
              </div>
            </div>

            {/* Currency toggle */}
            <div className="flex items-center gap-2 pt-2">
              <span className="text-xs text-slate-400">Display currency:</span>
              <button
                onClick={() => setCurrency("USD")}
                className={`px-2.5 py-1 rounded text-xs font-semibold ${currency === "USD" ? "bg-emerald-500 text-slate-950" : "bg-slate-800 text-slate-400"}`}
              >
                USD ($)
              </button>
              <button
                onClick={() => setCurrency("BDT")}
                className={`px-2.5 py-1 rounded text-xs font-semibold ${currency === "BDT" ? "bg-emerald-500 text-slate-950" : "bg-slate-800 text-slate-400"}`}
              >
                BDT (৳)
              </button>
            </div>
          </div>

          {/* Right Comparison Box */}
          <div className="lg:col-span-6 bg-slate-950/80 rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-xl space-y-6">
            <div className="grid grid-cols-2 gap-4 pb-6 border-b border-slate-850">
              <div>
                <span className="text-xs text-slate-400 block mb-1">Meta Official Cloud API</span>
                <span className="text-2xl font-bold text-red-400 font-mono line-through opacity-80">
                  {metaCostDisplay}
                </span>
                <span className="text-[11px] text-slate-500 block mt-1">Pay-per-message fees</span>
              </div>
              <div>
                <span className="text-xs text-emerald-400 font-semibold block mb-1">WhatsPulse SaaS Pro</span>
                <span className="text-2xl font-bold text-white font-mono">
                  {whatsPulseCostDisplay}
                </span>
                <span className="text-[11px] text-slate-400 block mt-1">Flat monthly subscription</span>
              </div>
            </div>

            {/* Total Savings Card */}
            <div className="p-4 rounded-xl bg-gradient-to-r from-emerald-950/40 to-teal-950/30 border border-emerald-500/30 flex items-center justify-between">
              <div>
                <span className="text-xs font-medium text-emerald-300 block">Net Monthly Savings:</span>
                <span className="text-3xl font-extrabold text-emerald-400 font-mono">
                  {savingsDisplay} <span className="text-xs font-bold uppercase text-emerald-300">/ month</span>
                </span>
              </div>
              <div className="text-right">
                <span className="inline-block px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-bold text-sm border border-emerald-500/30">
                  Save {percentageSaved}%
                </span>
              </div>
            </div>

            <ul className="space-y-2 text-xs text-slate-300">
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span>No per-message markup or surprise overage bills</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span>Unlimited multi-variant rotation to safeguard phone numbers</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span>Zero template approval delays &bull; Send instantly</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}

