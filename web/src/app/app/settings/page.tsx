"use client";

import { useState } from "react";
import {
  CreditCard,
  Shield,
  Key,
  Clock,
  CheckCircle2,
  Sliders,
  Sparkles,
  Zap
} from "lucide-react";

export default function SettingsPage() {
  const [minDelay, setMinDelay] = useState(5);
  const [maxDelay, setMaxDelay] = useState(12);
  const [apiKey, setApiKey] = useState("wp_live_8f912c9a92384781b0f19a");
  const [saved, setSaved] = useState(false);

  const handleSaveSettings = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>Settings &amp; Subscription</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Manage your SaaS subscription, throttle intervals, and API developer credentials.
        </p>
      </div>

      {/* Subscription Plan Card */}
      <div className="glass-panel p-6 sm:p-8 rounded-2xl border-2 border-emerald-500/40 shadow-2xl relative overflow-hidden bg-slate-950/70">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-850">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-white">Pro Academy Plan</span>
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-bold border border-emerald-500/20">
                Active Subscription
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              $49.00 / month &bull; Renews on Nov 30, 2026
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-300 font-semibold text-xs border border-slate-800 transition-colors">
              Manage Billing (Stripe)
            </button>
            <button className="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all">
              Upgrade to Agency
            </button>
          </div>
        </div>

        {/* Quota usage */}
        <div className="pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div>
            <span className="text-slate-400 block mb-1">Monthly Message Limit</span>
            <span className="text-base font-bold text-white font-mono">1,420 / 25,000</span>
          </div>
          <div>
            <span className="text-slate-400 block mb-1">WhatsApp Numbers Linked</span>
            <span className="text-base font-bold text-white font-mono">1 / 3 Devices</span>
          </div>
          <div>
            <span className="text-slate-400 block mb-1">Anti-Restriction Multi-SMS</span>
            <span className="text-base font-bold text-emerald-400">Unlimited Variants</span>
          </div>
        </div>
      </div>

      {/* Dispatch Throttle & Anti-Ban Speed Settings */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-400" />
            <span>Anti-Ban Throttle &amp; Jitter Interval</span>
          </h2>
          <span className="text-[11px] text-emerald-400 font-semibold">
            Recommended: 5–15 seconds
          </span>
        </div>

        <p className="text-xs text-slate-400">
          WhatsApp detects uniform robotic sending speeds. Adding a randomized delay between dispatches simulates organic human behavior.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 flex justify-between">
              <span>Minimum Random Delay:</span>
              <span className="text-emerald-400 font-mono">{minDelay} seconds</span>
            </label>
            <input
              type="range"
              min={2}
              max={15}
              value={minDelay}
              onChange={(e) => setMinDelay(Number(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer h-2 bg-slate-900 rounded-lg"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 flex justify-between">
              <span>Maximum Random Delay:</span>
              <span className="text-emerald-400 font-mono">{maxDelay} seconds</span>
            </label>
            <input
              type="range"
              min={minDelay + 1}
              max={30}
              value={maxDelay}
              onChange={(e) => setMaxDelay(Number(e.target.value))}
              className="w-full accent-emerald-500 cursor-pointer h-2 bg-slate-900 rounded-lg"
            />
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            onClick={handleSaveSettings}
            className="px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all flex items-center gap-1.5"
          >
            {saved ? <CheckCircle2 className="w-4 h-4" /> : null}
            <span>{saved ? "Settings Saved!" : "Save Throttle Settings"}</span>
          </button>
        </div>
      </div>

      {/* Developer API Key */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <h2 className="text-sm font-bold text-white flex items-center gap-2">
          <Key className="w-4 h-4 text-emerald-400" />
          <span>API Access &amp; Webhooks</span>
        </h2>
        <p className="text-xs text-slate-400">
          Trigger campaign dispatches programmatically from your student portal or coaching CRM.
        </p>

        <div className="flex items-center gap-2">
          <input
            type="text"
            readOnly
            value={apiKey}
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-300 font-mono"
          />
          <button
            onClick={() => {
              navigator.clipboard?.writeText(apiKey);
              alert("API Key copied to clipboard!");
            }}
            className="px-3.5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-300 font-semibold text-xs border border-slate-800 transition-colors"
          >
            Copy
          </button>
        </div>
      </div>
    </div>
  );
}
