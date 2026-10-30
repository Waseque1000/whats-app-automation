"use client";

import { useState } from "react";
import { Check, TrendingUp } from "lucide-react";

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
      <div className="bg-white rounded-3xl p-8 sm:p-12 border border-slate-200 shadow-xl relative overflow-hidden">
        {/* Soft emerald glow backdrop */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-50 rounded-full blur-3xl pointer-events-none" />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10">
          <div className="lg:col-span-6 space-y-6">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold">
              <TrendingUp className="w-3.5 h-3.5 text-emerald-600" />
              <span>Instant Cost Comparison</span>
            </div>

            <h2 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight leading-tight">
              Calculate Your <span className="text-emerald-600">Monthly Savings</span> vs Meta API
            </h2>

            <p className="text-slate-600 text-sm leading-relaxed">
              Meta charges for every single marketing conversation (~$0.025 - $0.035 each). With WhatsPulse, your team uses your own WhatsApp Web numbers with flat, predictable subscription pricing.
            </p>

            {/* Slider */}
            <div className="space-y-4 pt-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-slate-700">Monthly WhatsApp Messages:</span>
                <span className="text-lg font-bold text-emerald-600 font-mono">
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
                className="w-full accent-emerald-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
              />
              <div className="flex justify-between text-[11px] text-slate-400 font-medium">
                <span>2,000 / mo</span>
                <span>30,000 / mo</span>
                <span>60,000 / mo</span>
              </div>
            </div>

            {/* Currency toggle */}
            <div className="flex items-center gap-2 pt-2">
              <span className="text-xs text-slate-500 font-medium">Display currency:</span>
              <button
                onClick={() => setCurrency("USD")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${currency === "USD" ? "bg-emerald-600 text-white shadow-sm" : "bg-slate-100 text-slate-600 hover:bg-slate-200"}`}
              >
                USD ($)
              </button>
              <button
                onClick={() => setCurrency("BDT")}
                className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${currency === "BDT" ? "bg-emerald-600 text-white shadow-sm" : "bg-slate-100 text-slate-600 hover:bg-slate-200"}`}
              >
                BDT (৳)
              </button>
            </div>
          </div>

          {/* Right Comparison Box */}
          <div className="lg:col-span-6 bg-slate-50 rounded-2xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
            <div className="grid grid-cols-2 gap-4 pb-6 border-b border-slate-200">
              <div>
                <span className="text-xs text-slate-500 font-medium block mb-1">Meta Official Cloud API</span>
                <span className="text-2xl font-bold text-red-600 font-mono line-through opacity-80">
                  {metaCostDisplay}
                </span>
                <span className="text-[11px] text-slate-400 block mt-1">Pay-per-message fees</span>
              </div>
              <div>
                <span className="text-xs text-emerald-700 font-bold block mb-1">WhatsPulse SaaS Pro</span>
                <span className="text-2xl font-bold text-slate-900 font-mono">
                  {whatsPulseCostDisplay}
                </span>
                <span className="text-[11px] text-slate-500 block mt-1">Flat monthly subscription</span>
              </div>
            </div>

            {/* Total Savings Card */}
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 flex items-center justify-between">
              <div>
                <span className="text-xs font-semibold text-emerald-800 block">Net Monthly Savings:</span>
                <span className="text-3xl font-extrabold text-emerald-700 font-mono">
                  {savingsDisplay} <span className="text-xs font-bold uppercase text-emerald-700">/ month</span>
                </span>
              </div>
              <div className="text-right">
                <span className="inline-block px-3 py-1 rounded-full bg-emerald-600 text-white font-bold text-sm shadow-sm">
                  Save {percentageSaved}%
                </span>
              </div>
            </div>

            <ul className="space-y-2.5 text-xs text-slate-700 font-medium">
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                <span>No per-message markup or surprise overage bills</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                <span>Unlimited multi-variant rotation to safeguard phone numbers</span>
              </li>
              <li className="flex items-center gap-2">
                <Check className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                <span>Zero template approval delays &bull; Send instantly</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  );
}
