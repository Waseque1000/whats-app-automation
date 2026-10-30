"use client";

import Link from "next/link";
import {
  Send,
  Users,
  ShieldCheck,
  AlertCircle,
  TrendingUp,
  Smartphone,
  ArrowRight,
  CheckCircle2,
  Clock,
  Plus
} from "lucide-react";
import { INITIAL_CAMPAIGNS, INITIAL_STUDENTS, INITIAL_DEVICE_SESSION } from "../../lib/mock-data";

export default function DashboardOverviewPage() {
  const totalSent = INITIAL_CAMPAIGNS.reduce((acc, c) => acc + c.sentCount, 0);
  const totalSkipped = INITIAL_CAMPAIGNS.reduce((acc, c) => acc + c.skippedCount, 0);

  return (
    <div className="space-y-8">
      {/* Header banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Dashboard Overview
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Real-time campaign health, anti-restriction rotation metrics, and connected device status.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/app/students"
            className="px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-300 font-semibold text-xs border border-slate-800 transition-colors"
          >
            Import Students
          </Link>
          <Link
            href="/app/campaigns"
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>New Anti-Ban Campaign</span>
          </Link>
        </div>
      </div>

      {/* 4 Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Total Delivered</span>
            <div className="w-7 h-7 rounded-lg bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-white font-mono">{totalSent}</div>
          <span className="text-[11px] text-emerald-400 flex items-center gap-1 font-medium">
            <TrendingUp className="w-3 h-3" /> +100% inbox deliverability
          </span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Auto-Skipped (No WA)</span>
            <div className="w-7 h-7 rounded-lg bg-amber-500/10 text-amber-400 flex items-center justify-center">
              <AlertCircle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-amber-400 font-mono">{totalSkipped}</div>
          <span className="text-[11px] text-slate-400">
            Zero stall delay &bull; Status saved
          </span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Total Contacts</span>
            <div className="w-7 h-7 rounded-lg bg-indigo-500/10 text-indigo-400 flex items-center justify-center">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-white font-mono">{INITIAL_STUDENTS.length}</div>
          <span className="text-[11px] text-slate-400">
            Across 2 coaching batches
          </span>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-slate-400">Anti-Restriction Shield</span>
            <div className="w-7 h-7 rounded-lg bg-teal-500/10 text-teal-400 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-teal-300 font-mono">100%</div>
          <span className="text-[11px] text-teal-400">
            Sequential round-robin active
          </span>
        </div>
      </div>

      {/* Device Connection + Quick Launcher */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Active WhatsApp Device Card */}
        <div className="lg:col-span-5 glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-bold text-sm text-white flex items-center gap-2">
              <Smartphone className="w-4 h-4 text-emerald-400" />
              <span>Connected WhatsApp Phone</span>
            </h2>
            <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] font-bold border border-emerald-500/20">
              Session Ready
            </span>
          </div>

          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-850 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">Phone Number:</span>
              <span className="text-xs font-mono font-bold text-white">{INITIAL_DEVICE_SESSION.phoneNumber}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">Device Battery:</span>
              <span className="text-xs font-semibold text-emerald-400">{INITIAL_DEVICE_SESSION.batteryLevel}% (Charging)</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">Cloud Worker:</span>
              <span className="text-xs text-slate-300">{INITIAL_DEVICE_SESSION.browser}</span>
            </div>
          </div>

          <div className="pt-1 flex items-center justify-between">
            <Link
              href="/app/connect"
              className="text-xs font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
            >
              Manage Session or Scan New QR <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* Quick Campaign Callout */}
        <div className="lg:col-span-7 glass-panel p-6 rounded-2xl border border-slate-800 flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-[11px] font-semibold border border-emerald-500/20">
              <ShieldCheck className="w-3.5 h-3.5" /> Anti-Restriction Rotation Engine
            </div>
            <h2 className="text-lg font-bold text-white">Create Multi-SMS Broadcast</h2>
            <p className="text-xs text-slate-400 leading-relaxed">
              Configure 3 to 5 message variations in our live tabbed studio. The system automatically alternates between SMS #1, SMS #2, and SMS #3 to prevent account bans.
            </p>
          </div>

          <div className="pt-2 flex items-center gap-3">
            <Link
              href="/app/campaigns"
              className="px-5 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all flex items-center gap-2"
            >
              <Send className="w-4 h-4 fill-slate-950" />
              <span>Launch Campaign Studio</span>
            </Link>
            <Link
              href="/app/templates"
              className="px-4 py-3 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-300 font-semibold text-xs border border-slate-800 transition-colors"
            >
              Browse Templates
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Campaigns Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="font-bold text-sm text-white flex items-center gap-2">
            <Clock className="w-4 h-4 text-emerald-400" />
            <span>Recent Campaign Dispatches</span>
          </h2>
          <Link href="/app/reports" className="text-xs text-emerald-400 hover:underline">
            View All Reports &rarr;
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                <th className="pb-3 px-3">Campaign Name</th>
                <th className="pb-3 px-3">Created Date</th>
                <th className="pb-3 px-3">Recipients</th>
                <th className="pb-3 px-3">Delivered</th>
                <th className="pb-3 px-3">Auto-Skipped</th>
                <th className="pb-3 px-3">Anti-Ban Variants</th>
                <th className="pb-3 px-3 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {INITIAL_CAMPAIGNS.map((camp) => (
                <tr key={camp.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="py-3 px-3 font-semibold text-white">{camp.name}</td>
                  <td className="py-3 px-3 text-slate-400">{camp.createdAt}</td>
                  <td className="py-3 px-3 font-mono text-slate-300">{camp.totalRecipients}</td>
                  <td className="py-3 px-3 font-mono text-emerald-400 font-semibold">{camp.sentCount}</td>
                  <td className="py-3 px-3 font-mono text-amber-400">{camp.skippedCount}</td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700 text-[10px]">
                      {camp.variants.length} SMS Designs
                    </span>
                  </td>
                  <td className="py-3 px-3 text-right">
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold text-[10px] border border-emerald-500/20">
                      <CheckCircle2 className="w-3 h-3" /> Completed
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

