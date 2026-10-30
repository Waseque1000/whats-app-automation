"use client";

import { useState } from "react";
import {
  Key,
  CheckCircle2,
  Sliders
} from "lucide-react";

export default function SettingsPage() {
  const [minDelay, setMinDelay] = useState(5);
  const [maxDelay, setMaxDelay] = useState(12);
  const [apiKey] = useState("wp_live_8f912c9a92384781b0f19a");
  const [saved, setSaved] = useState(false);

  const handleSaveSettings = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
          <span>Settings &amp; Subscription</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Manage your SaaS subscription, throttle intervals, and API developer credentials.
        </p>
      </div>

      {/* Subscription Plan Card */}
      <div className="bg-white p-6 sm:p-8 rounded-3xl border-2 border-emerald-500 shadow-xl relative overflow-hidden">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-bold text-slate-900">Pro Academy Plan</span>
              <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-200">
                Active Subscription
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-medium">
              $49.00 / month &bull; Renews on Nov 30, 2026
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button className="px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs border border-slate-200 transition-colors">
              Manage Billing (Stripe)
            </button>
            <button className="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition-all">
              Upgrade to Agency
            </button>
          </div>
        </div>

        {/* Quota usage */}
        <div className="pt-6 grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div>
            <span className="text-slate-500 font-medium block mb-1">Monthly Message Limit</span>
            <span className="text-base font-bold text-slate-900 font-mono">1,420 / 25,000</span>
          </div>
          <div>
            <span className="text-slate-500 font-medium block mb-1">WhatsApp Numbers Linked</span>
            <span className="text-base font-bold text-slate-900 font-mono">1 / 3 Devices</span>
          </div>
          <div>
            <span className="text-slate-500 font-medium block mb-1">Anti-Restriction Multi-SMS</span>
            <span className="text-base font-bold text-emerald-700">Unlimited Variants</span>
          </div>
        </div>
      </div>

      {/* Dispatch Throttle & Anti-Ban Speed Settings */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Sliders className="w-4 h-4 text-emerald-600" />
            <span>Anti-Ban Throttle &amp; Jitter Interval</span>
          </h2>
          <span className="text-[11px] text-emerald-700 font-bold">
            Recommended: 5–15 seconds
          </span>
        </div>

        <p className="text-xs text-slate-600 font-medium">
          WhatsApp detects uniform robotic sending speeds. Adding a randomized delay between dispatches simulates organic human behavior.
        </p>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-700 flex justify-between">
              <span>Minimum Random Delay:</span>
              <span className="text-emerald-700 font-mono">{minDelay} seconds</span>
            </label>
            <input
              type="range"
              min={2}
              max={15}
              value={minDelay}
              onChange={(e) => setMinDelay(Number(e.target.value))}
              className="w-full accent-emerald-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
            />
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-700 flex justify-between">
              <span>Maximum Random Delay:</span>
              <span className="text-emerald-700 font-mono">{maxDelay} seconds</span>
            </label>
            <input
              type="range"
              min={minDelay + 1}
              max={30}
              value={maxDelay}
              onChange={(e) => setMaxDelay(Number(e.target.value))}
              className="w-full accent-emerald-600 cursor-pointer h-2 bg-slate-200 rounded-lg"
            />
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            onClick={handleSaveSettings}
            className="px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition-all flex items-center gap-1.5"
          >
            {saved ? <CheckCircle2 className="w-4 h-4" /> : null}
            <span>{saved ? "Settings Saved!" : "Save Throttle Settings"}</span>
          </button>
        </div>
      </div>

      {/* Developer API Key */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
        <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
          <Key className="w-4 h-4 text-emerald-600" />
          <span>API Access &amp; Webhooks</span>
        </h2>
        <p className="text-xs text-slate-600 font-medium">
          Trigger campaign dispatches programmatically from your student portal or coaching CRM.
        </p>

        <div className="flex items-center gap-2">
          <input
            type="text"
            readOnly
            value={apiKey}
            className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs text-slate-700 font-mono font-semibold"
          />
          <button
            onClick={() => {
              navigator.clipboard?.writeText(apiKey);
              alert("API Key copied to clipboard!");
            }}
            className="px-3.5 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs border border-slate-200 transition-colors"
          >
            Copy
          </button>
        </div>
      </div>
    </div>
  );
}
