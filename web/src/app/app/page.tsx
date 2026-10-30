"use client";

import Link from "next/link";
import {
  Users,
  ShieldCheck,
  AlertCircle,
  TrendingUp,
  Smartphone,
  ArrowRight,
  CheckCircle2,
  Clock,
  Plus,
  Send
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
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Dashboard Overview
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Real-time campaign health, anti-restriction rotation metrics, and connected device status.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/app/students"
            className="px-4 py-2.5 rounded-xl bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs border border-slate-200 shadow-sm transition-colors"
          >
            Import Students
          </Link>
          <Link
            href="/app/campaigns"
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>New Anti-Ban Campaign</span>
          </Link>
        </div>
      </div>

      {/* 4 Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Total Delivered</span>
            <div className="w-7 h-7 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-slate-900 font-mono">{totalSent}</div>
          <span className="text-[11px] text-emerald-700 flex items-center gap-1 font-bold">
            <TrendingUp className="w-3 h-3" /> +100% inbox deliverability
          </span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Auto-Skipped (No WA)</span>
            <div className="w-7 h-7 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
              <AlertCircle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-amber-600 font-mono">{totalSkipped}</div>
          <span className="text-[11px] text-slate-500 font-medium">
            Zero stall delay &bull; Status saved
          </span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Total Contacts</span>
            <div className="w-7 h-7 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-slate-900 font-mono">{INITIAL_STUDENTS.length}</div>
          <span className="text-[11px] text-slate-500 font-medium">
            Across 2 coaching batches
          </span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500">Anti-Restriction Shield</span>
            <div className="w-7 h-7 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center font-bold">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="text-3xl font-extrabold text-teal-700 font-mono">100%</div>
          <span className="text-[11px] text-teal-700 font-bold">
            Sequential round-robin active
          </span>
        </div>
      </div>

      {/* Device Connection + Quick Launcher */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Active WhatsApp Device Card */}
        <div className="lg:col-span-5 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="font-bold text-sm text-slate-900 flex items-center gap-2">
              <Smartphone className="w-4 h-4 text-emerald-600" />
              <span>Connected WhatsApp Phone</span>
            </h2>
            <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-200">
              Session Ready
            </span>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">Phone Number:</span>
              <span className="text-xs font-mono font-bold text-slate-900">{INITIAL_DEVICE_SESSION.phoneNumber}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">Device Battery:</span>
              <span className="text-xs font-bold text-emerald-700">{INITIAL_DEVICE_SESSION.batteryLevel}% (Charging)</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-500">Cloud Worker:</span>
              <span className="text-xs text-slate-700 font-medium">{INITIAL_DEVICE_SESSION.browser}</span>
            </div>
          </div>

          <div className="pt-1 flex items-center justify-between">
            <Link
              href="/app/connect"
              className="text-xs font-bold text-emerald-700 hover:text-emerald-800 flex items-center gap-1"
            >
              Manage Session or Scan New QR <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {/* Quick Campaign Callout */}
        <div className="lg:col-span-7 bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex flex-col justify-between space-y-4">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 text-[11px] font-bold border border-emerald-200">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> Anti-Restriction Rotation Engine
            </div>
            <h2 className="text-lg font-bold text-slate-900">Create Multi-SMS Broadcast</h2>
            <p className="text-xs text-slate-600 leading-relaxed">
              Configure 3 to 5 message variations in our live tabbed studio. The system automatically alternates between SMS #1, SMS #2, and SMS #3 to prevent account bans.
            </p>
          </div>

          <div className="pt-2 flex items-center gap-3">
            <Link
              href="/app/campaigns"
              className="px-5 py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition-all flex items-center gap-2"
            >
              <Send className="w-4 h-4 fill-white" />
              <span>Launch Campaign Studio</span>
            </Link>
            <Link
              href="/app/templates"
              className="px-4 py-3 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs border border-slate-200 transition-colors"
            >
              Browse Templates
            </Link>
          </div>
        </div>
      </div>

      {/* Recent Campaigns Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="font-bold text-sm text-slate-900 flex items-center gap-2">
            <Clock className="w-4 h-4 text-emerald-600" />
            <span>Recent Campaign Dispatches</span>
          </h2>
          <Link href="/app/reports" className="text-xs font-bold text-emerald-700 hover:underline">
            View All Reports &rarr;
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 font-bold bg-slate-50/50">
                <th className="py-3 px-3">Campaign Name</th>
                <th className="py-3 px-3">Created Date</th>
                <th className="py-3 px-3">Recipients</th>
                <th className="py-3 px-3">Delivered</th>
                <th className="py-3 px-3">Auto-Skipped</th>
                <th className="py-3 px-3">Anti-Ban Variants</th>
                <th className="py-3 px-3 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {INITIAL_CAMPAIGNS.map((camp) => (
                <tr key={camp.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3.5 px-3 font-bold text-slate-900">{camp.name}</td>
                  <td className="py-3.5 px-3 text-slate-500 font-medium">{camp.createdAt}</td>
                  <td className="py-3.5 px-3 font-mono text-slate-700">{camp.totalRecipients}</td>
                  <td className="py-3.5 px-3 font-mono text-emerald-700 font-bold">{camp.sentCount}</td>
                  <td className="py-3.5 px-3 font-mono text-amber-600 font-bold">{camp.skippedCount}</td>
                  <td className="py-3.5 px-3">
                    <span className="px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200 text-[10px] font-semibold">
                      {camp.variants.length} SMS Designs
                    </span>
                  </td>
                  <td className="py-3.5 px-3 text-right">
                    <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 font-bold text-[10px] border border-emerald-200">
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
