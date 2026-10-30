"use client";

import { useState } from "react";
import { BarChart3, Download, CheckCircle2, AlertCircle, FileSpreadsheet, Calendar } from "lucide-react";
import { INITIAL_CAMPAIGNS } from "../../../lib/mock-data";

export default function ReportsPage() {
  const [selectedCampaign, setSelectedCampaign] = useState<string>("All");

  const totalDelivered = INITIAL_CAMPAIGNS.reduce((acc, c) => acc + c.sentCount, 0);
  const totalSkipped = INITIAL_CAMPAIGNS.reduce((acc, c) => acc + c.skippedCount, 0);
  const totalCandidates = INITIAL_CAMPAIGNS.reduce((acc, c) => acc + c.totalRecipients, 0);
  const successRate = Math.round((totalDelivered / Math.max(totalCandidates, 1)) * 100);

  const handleDownloadAuditReport = (campName: string) => {
    const csvContent = `Campaign,Recipients,Delivered,AutoSkipped,Status\n"${campName}",17,15,2,"Completed"\n`;
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Audit_Report_${campName.replace(/\s+/g, '_')}.csv`;
    a.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <span>Campaign Reports &amp; Delivery Audit</span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Historical delivery metrics, non-WhatsApp auto-skip breakdown, and exportable CSV audit trails.
          </p>
        </div>
      </div>

      {/* Summary Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Total Broadcasted</span>
          <span className="text-2xl font-bold font-mono text-white">{totalCandidates}</span>
        </div>
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <span className="text-xs text-emerald-400 block mb-1">Delivered to Inbox</span>
          <span className="text-2xl font-bold font-mono text-emerald-400">{totalDelivered}</span>
        </div>
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <span className="text-xs text-amber-400 block mb-1">Auto-Skipped (No WA)</span>
          <span className="text-2xl font-bold font-mono text-amber-400">{totalSkipped}</span>
        </div>
        <div className="glass-panel p-5 rounded-2xl border border-slate-800">
          <span className="text-xs text-teal-300 block mb-1">Deliverability Rate</span>
          <span className="text-2xl font-bold font-mono text-teal-300">{successRate}%</span>
        </div>
      </div>

      {/* Campaign Logs Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-white">All Completed Campaigns</h2>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold bg-slate-950/40">
                <th className="py-3 px-4">Campaign Name</th>
                <th className="py-3 px-4">Dispatch Date</th>
                <th className="py-3 px-4">Total</th>
                <th className="py-3 px-4">Delivered</th>
                <th className="py-3 px-4">Skipped (No WA)</th>
                <th className="py-3 px-4">Anti-Ban Variants</th>
                <th className="py-3 px-4 text-right">Audit CSV</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {INITIAL_CAMPAIGNS.map((camp) => (
                <tr key={camp.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="py-3.5 px-4 font-semibold text-white">{camp.name}</td>
                  <td className="py-3.5 px-4 text-slate-400 flex items-center gap-1.5">
                    <Calendar className="w-3.5 h-3.5 text-slate-500" />
                    <span>{camp.createdAt}</span>
                  </td>
                  <td className="py-3.5 px-4 font-mono text-slate-300">{camp.totalRecipients}</td>
                  <td className="py-3.5 px-4 font-mono text-emerald-400 font-bold">{camp.sentCount}</td>
                  <td className="py-3.5 px-4 font-mono text-amber-400">{camp.skippedCount}</td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 rounded bg-slate-850 text-slate-300 border border-slate-750 text-[10px]">
                      {camp.variants.length} SMS Designs
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => handleDownloadAuditReport(camp.name)}
                      className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-850 text-slate-300 hover:text-white border border-slate-800 text-xs transition-colors"
                    >
                      <Download className="w-3 h-3 text-emerald-400" />
                      <span>Export</span>
                    </button>
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

