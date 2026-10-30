"use client";

import { useState } from "react";
import {
  Plus,
  Trash2,
  ShieldCheck,
  CheckCircle2,
  AlertCircle,
  Download,
  Users,
  Eye
} from "lucide-react";
import { INITIAL_STUDENTS } from "../../../lib/mock-data";
import { renderStudentMessage } from "../../../lib/spintax";
import { CampaignRecipient } from "../../../types";

export default function CampaignsPage() {
  const [activeTab, setActiveTab] = useState<"composer" | "monitor">("composer");
  const [campaignName, setCampaignName] = useState("Ass-7 Durber Final Notice");
  const [selectedBatch, setSelectedBatch] = useState("All");

  // Multi-SMS Variants State
  const [variants, setVariants] = useState<string[]>([
    "{হ্যালো|প্রিয়} {name}! তোমার অ্যাসাইনমেন্ট জমা দেওয়ার শেষ তারিখ আগামী রবিবার। সময়মতো সাবমিট করো।",
    "আসসালামু আলাইকুম {name}, আশা করি ভালো আছো। মনে করিয়ে দিচ্ছি যে আমাদের পরবর্তী ক্লাস টেস্ট আগামী সোমবার।",
    "{Hey|Hello} {name}! অনুগ্রহ করে তোমার রোল {roll}-এর অ্যাসাইনমেন্ট আগামীকালের মধ্যে কমপ্লিট করে ফেলো।"
  ]);
  const [activeVariantTab, setActiveVariantTab] = useState(0);

  // Review modal state
  const [reviewModalOpen, setReviewModalOpen] = useState(false);
  const [consentConfirmed, setConsentConfirmed] = useState(true);

  // Dispatch monitor state
  const [isExecuting, setIsExecuting] = useState(false);
  const [progress, setProgress] = useState(0);
  const [queue, setQueue] = useState<CampaignRecipient[]>([]);

  // Filter students based on batch selection
  const filteredStudents = selectedBatch === "All"
    ? INITIAL_STUDENTS
    : INITIAL_STUDENTS.filter(s => s.batch === selectedBatch);

  // Add new SMS design tab
  const handleAddVariant = () => {
    if (variants.length >= 6) {
      alert("Maximum 6 variations recommended for optimal delivery.");
      return;
    }
    const newVariants = [...variants, `Variant #${variants.length + 1}: Hello {name}, important update regarding your class.`];
    setVariants(newVariants);
    setActiveVariantTab(newVariants.length - 1);
  };

  // Remove SMS design tab
  const handleRemoveVariant = (index: number) => {
    if (variants.length <= 1) {
      alert("At least 1 SMS variation is required.");
      return;
    }
    const newVariants = variants.filter((_, i) => i !== index);
    setVariants(newVariants);
    setActiveVariantTab(Math.max(0, activeVariantTab - 1));
  };

  // Insert placeholder token into current variant text
  const insertToken = (token: string) => {
    const current = variants[activeVariantTab];
    const updated = current + " " + token;
    const newVariants = [...variants];
    newVariants[activeVariantTab] = updated;
    setVariants(newVariants);
  };

  // Prepare & Launch campaign
  const handleLaunchCampaign = () => {
    setReviewModalOpen(false);
    setActiveTab("monitor");
    setIsExecuting(true);
    setProgress(0);

    // Build initial queue with round-robin variants
    const initialQueue: CampaignRecipient[] = filteredStudents.map((st, i) => {
      const vIdx = i % variants.length;
      return {
        id: i + 1,
        studentId: st.id,
        name: st.name,
        phone: st.phone,
        variantIndex: vIdx,
        smsVariant: `SMS #${vIdx + 1}`,
        personalizedMessage: renderStudentMessage(variants[vIdx], st, i),
        status: "pending",
      };
    });

    setQueue(initialQueue);

    // Simulate real-time dispatch progress with auto-skipping
    let currentStep = 0;
    const interval = setInterval(() => {
      currentStep++;
      if (currentStep > initialQueue.length) {
        clearInterval(interval);
        setIsExecuting(false);
        setProgress(100);
        return;
      }

      setQueue((prevQueue) => {
        return prevQueue.map((rec, idx) => {
          if (idx < currentStep) {
            const student = filteredStudents[idx];
            const isNoWhatsApp = student.whatsappStatus === "inactive" || student.phone.includes("673") || student.phone.includes("455");
            return {
              ...rec,
              status: isNoWhatsApp ? "skipped" : "sent",
              sentAt: new Date().toLocaleTimeString(),
              errorMessage: isNoWhatsApp ? "Number has no WhatsApp account (Auto-Skipped)" : undefined
            };
          }
          return rec;
        });
      });

      setProgress(Math.round((currentStep / initialQueue.length) * 100));
    }, 600);
  };

  // Export current campaign to CSV
  const handleExportCsv = () => {
    const headers = "Recipient ID,Name,Phone,SMS Variant,Status,Sent At,Message\n";
    const rows = queue.map(q => `"${q.id}","${q.name}","${q.phone}","${q.smsVariant}","${q.status}","${q.sentAt || ''}","${q.personalizedMessage.replace(/"/g, '""')}"`).join("\n");
    const blob = new Blob([headers + rows], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${campaignName.replace(/\s+/g, '_')}_Report.csv`;
    a.click();
  };

  const sentCount = queue.filter(q => q.status === "sent").length;
  const skippedCount = queue.filter(q => q.status === "skipped").length;

  return (
    <div className="space-y-6">
      {/* Top Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <span>Campaigns &amp; Anti-Ban Studio</span>
            <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
              Round-Robin v2.4
            </span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Build multi-variation SMS designs that rotate automatically to bypass WhatsApp spam rate limits.
          </p>
        </div>

        {/* Tab switch between Composer and Dispatch Monitor */}
        <div className="flex items-center gap-1.5 p-1 rounded-2xl bg-white border border-slate-200 text-xs font-bold shadow-sm">
          <button
            onClick={() => setActiveTab("composer")}
            className={`px-4 py-2 rounded-xl transition-all ${
              activeTab === "composer" ? "bg-emerald-600 text-white font-bold shadow-sm" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            1. Campaign Studio
          </button>
          <button
            onClick={() => setActiveTab("monitor")}
            className={`px-4 py-2 rounded-xl flex items-center gap-1.5 transition-all ${
              activeTab === "monitor" ? "bg-emerald-600 text-white font-bold shadow-sm" : "text-slate-600 hover:text-slate-900"
            }`}
          >
            <span>2. Dispatch Monitor</span>
            {isExecuting && <span className="w-2 h-2 rounded-full bg-white animate-ping" />}
          </button>
        </div>
      </div>

      {activeTab === "composer" ? (
        <div className="space-y-6">
          {/* Campaign Configuration Card */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Users className="w-4 h-4 text-emerald-600" />
              <span>Step 1: Campaign Name &amp; Target Batch</span>
            </h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1.5">Campaign Name</label>
                <input
                  type="text"
                  value={campaignName}
                  onChange={(e) => setCampaignName(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors"
                  placeholder="e.g. Weekly Exam Alert"
                />
              </div>

              <div>
                <label className="text-xs font-bold text-slate-700 block mb-1.5">Select Student Batch</label>
                <select
                  value={selectedBatch}
                  onChange={(e) => setSelectedBatch(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs text-slate-900 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors"
                >
                  <option value="All">All Students ({INITIAL_STUDENTS.length} contacts)</option>
                  <option value="Ass-7 Durber">Ass-7 Durber Batch (4 contacts)</option>
                  <option value="Batch-2026">Batch-2026 (6 contacts)</option>
                </select>
              </div>
            </div>

            <div className="pt-2 flex items-center justify-between text-xs text-slate-500">
              <span className="flex items-center gap-1.5 text-emerald-700 font-bold">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Target: <strong>{filteredStudents.length} eligible recipients</strong> selected</span>
              </span>
              <span className="text-[11px] text-slate-400">
                Non-WhatsApp numbers will auto-skip without delaying queue
              </span>
            </div>
          </div>

          {/* Multi-SMS Variation Studio */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-600" />
                  <span>Step 2: Message Variations Studio (Anti-Restriction Active)</span>
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  The system rotates sequentially between these variations to ensure no two consecutive messages look identical.
                </p>
              </div>

              <button
                onClick={handleAddVariant}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 text-xs font-bold transition-colors"
              >
                <Plus className="w-3.5 h-3.5" />
                <span>+ Add SMS Design</span>
              </button>
            </div>

            {/* Dynamic Variant Tabs */}
            <div className="flex items-center space-x-2 border-b border-slate-100 pb-2 overflow-x-auto">
              {variants.map((_, idx) => (
                <div key={idx} className="flex items-center">
                  <button
                    onClick={() => setActiveVariantTab(idx)}
                    className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition-all ${
                      activeVariantTab === idx
                        ? "bg-emerald-600 text-white shadow-sm"
                        : "bg-slate-100 text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    SMS #{idx + 1}
                  </button>
                  {variants.length > 1 && (
                    <button
                      onClick={() => handleRemoveVariant(idx)}
                      className="ml-1 p-1 text-slate-400 hover:text-red-500 transition-colors"
                      title="Delete this variant"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              ))}
            </div>

            {/* Variant Message Editor */}
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>Message text for <strong className="text-slate-900">SMS #{activeVariantTab + 1}</strong>:</span>
                <span className="text-[11px] font-mono text-slate-400 font-medium">
                  {variants[activeVariantTab].length} chars
                </span>
              </div>

              <textarea
                rows={5}
                value={variants[activeVariantTab]}
                onChange={(e) => {
                  const updated = [...variants];
                  updated[activeVariantTab] = e.target.value;
                  setVariants(updated);
                }}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-xs sm:text-sm text-slate-900 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors font-sans leading-relaxed"
              />

              {/* Variable Chips Bar */}
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span className="text-slate-400 text-[11px] font-medium">Insert Tag:</span>
                <button
                  type="button"
                  onClick={() => insertToken("{name}")}
                  className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 text-[11px] font-bold"
                >
                  + &#123;name&#125;
                </button>
                <button
                  type="button"
                  onClick={() => insertToken("{roll}")}
                  className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 text-[11px] font-bold"
                >
                  + &#123;roll&#125;
                </button>
                <button
                  type="button"
                  onClick={() => insertToken("{batch}")}
                  className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 text-[11px] font-bold"
                >
                  + &#123;batch&#125;
                </button>
                <button
                  type="button"
                  onClick={() => insertToken("{Hello|Hi|Dear}")}
                  className="px-2.5 py-1 rounded-lg bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 text-[11px] font-bold"
                >
                  + Spintax &#123;Hello|Hi|Dear&#125;
                </button>
              </div>
            </div>
          </div>

          {/* Step 3: Multi-Student Rotation Preview */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                  <Eye className="w-4 h-4 text-emerald-600" />
                  <span>Step 3: Multi-Student Sequential Rotation Preview</span>
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  Preview how consecutive recipients receive different designs in round-robin order.
                </p>
              </div>
              <span className="text-[11px] font-mono text-emerald-700 font-bold px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200">
                Pattern: {variants.map((_, i) => `SMS #${i+1}`).join(" ➔ ")} ➔ ...
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {filteredStudents.slice(0, 3).map((st, i) => {
                const vIdx = i % variants.length;
                return (
                  <div key={st.id} className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                    <div className="flex items-center justify-between text-xs">
                      <span className="font-bold text-slate-900">{st.name}</span>
                      <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 text-[10px] font-bold">
                        SMS #{vIdx + 1}
                      </span>
                    </div>
                    <p className="text-xs text-slate-700 leading-relaxed bg-white p-3 rounded-xl border border-slate-200 shadow-xs">
                      {renderStudentMessage(variants[vIdx], st, i)}
                    </p>
                  </div>
                );
              })}
            </div>

            {/* Launch Action */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-end">
              <button
                onClick={() => setReviewModalOpen(true)}
                className="flex items-center gap-2 px-6 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs shadow-md shadow-emerald-600/20 transition-all hover:scale-[1.02] active:scale-[0.98]"
              >
                <span>Review &amp; Confirm Campaign &rarr;</span>
              </button>
            </div>
          </div>
        </div>
      ) : (
        /* Dispatch Monitor Tab */
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <span>Campaign: {campaignName}</span>
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                    isExecuting ? "bg-emerald-100 text-emerald-800 border border-emerald-300" : progress === 100 ? "bg-slate-100 text-slate-800" : "bg-slate-100 text-slate-600"
                  }`}>
                    {isExecuting ? "● Dispatching" : progress === 100 ? "✓ Completed" : "Ready"}
                  </span>
                </h2>
                <span className="text-xs text-slate-500">
                  {variants.length} SMS Designs rotating &bull; Total Candidates: {queue.length}
                </span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleExportCsv}
                  disabled={queue.length === 0}
                  className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs border border-slate-200 transition-colors flex items-center gap-1.5 disabled:opacity-50"
                >
                  <Download className="w-3.5 h-3.5" />
                  <span>Download CSV Report</span>
                </button>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="space-y-2 pt-2">
              <div className="flex items-center justify-between text-xs text-slate-500 font-semibold">
                <span>Dispatch Progress:</span>
                <span className="font-mono font-bold text-emerald-700">{progress}%</span>
              </div>
              <div className="w-full h-3 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                <div
                  className="h-full bg-emerald-600 transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>

            {/* Stats Row */}
            <div className="grid grid-cols-3 gap-4 pt-2">
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-[11px] text-slate-500 font-semibold block">Delivered Messages</span>
                <span className="text-xl font-bold font-mono text-emerald-700">{sentCount}</span>
              </div>
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-[11px] text-slate-500 font-semibold block">Auto-Skipped (No WA)</span>
                <span className="text-xl font-bold font-mono text-amber-600">{skippedCount}</span>
              </div>
              <div className="p-3.5 rounded-2xl bg-slate-50 border border-slate-200">
                <span className="text-[11px] text-slate-500 font-semibold block">Pending Queue</span>
                <span className="text-xl font-bold font-mono text-slate-700">{queue.length - sentCount - skippedCount}</span>
              </div>
            </div>
          </div>

          {/* Live Queue Table */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="font-bold text-sm text-slate-900">Live Recipient Queue Log</h3>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 font-bold bg-slate-50">
                    <th className="py-3 px-3">#</th>
                    <th className="py-3 px-3">Student Name</th>
                    <th className="py-3 px-3">Phone</th>
                    <th className="py-3 px-3">Assigned Variant</th>
                    <th className="py-3 px-3">Sent Time</th>
                    <th className="py-3 px-3 text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {queue.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="py-8 text-center text-slate-400 font-medium">
                        No active dispatch. Click &ldquo;1. Campaign Studio&rdquo; and click &ldquo;Review &amp; Confirm&rdquo; to launch.
                      </td>
                    </tr>
                  ) : (
                    queue.map((item) => (
                      <tr key={item.id} className="hover:bg-slate-50/60 transition-colors">
                        <td className="py-3.5 px-3 font-mono text-slate-400">{item.id}</td>
                        <td className="py-3.5 px-3 font-bold text-slate-900">{item.name}</td>
                        <td className="py-3.5 px-3 font-mono text-slate-600">{item.phone}</td>
                        <td className="py-3.5 px-3">
                          <span className="px-2.5 py-0.5 rounded-full bg-slate-100 text-emerald-700 border border-slate-200 text-[10px] font-bold">
                            {item.smsVariant}
                          </span>
                        </td>
                        <td className="py-3.5 px-3 font-mono text-slate-500">{item.sentAt || "—"}</td>
                        <td className="py-3.5 px-3 text-right">
                          {item.status === "sent" ? (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-[10px] font-bold border border-emerald-200">
                              <CheckCircle2 className="w-3 h-3" /> Delivered
                            </span>
                          ) : item.status === "skipped" ? (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 text-[10px] font-bold border border-amber-200">
                              <AlertCircle className="w-3 h-3" /> Auto-Skipped (No WA)
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-500 text-[10px] font-medium">
                              Pending
                            </span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* Confirmation Modal */}
      {reviewModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-lg rounded-3xl p-6 border border-slate-200 shadow-2xl space-y-5 animate-in fade-in zoom-in-95">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span>Campaign Review &amp; Anti-Restriction Launch</span>
              </h3>
            </div>

            <div className="space-y-3 text-xs text-slate-600">
              <div className="p-4 rounded-2xl bg-slate-50 border border-slate-200 space-y-2">
                <div className="flex justify-between">
                  <span className="text-slate-500">Campaign Name:</span>
                  <strong className="text-slate-900">{campaignName}</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Total Recipients:</span>
                  <strong className="text-slate-900">{filteredStudents.length} Students</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Anti-Restriction Variants:</span>
                  <strong className="text-emerald-700">{variants.length} SMS Designs Active</strong>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Invalid Number Handling:</span>
                  <strong className="text-teal-700">Auto-Skip (No Stalls)</strong>
                </div>
              </div>

              {/* Policy Consent checkbox */}
              <label className="flex items-center gap-2.5 pt-2 cursor-pointer select-none">
                <input
                  type="checkbox"
                  checked={consentConfirmed}
                  onChange={(e) => setConsentConfirmed(e.target.checked)}
                  className="w-4 h-4 rounded text-emerald-600 accent-emerald-600 bg-white border-slate-300 cursor-pointer"
                />
                <span className="text-xs text-slate-700 font-semibold">
                  ✓ I confirm recipient consent &amp; WhatsApp communication compliance
                </span>
              </label>
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-3">
              <button
                onClick={() => setReviewModalOpen(false)}
                className="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 hover:text-slate-900 text-xs font-bold"
              >
                Cancel
              </button>
              <button
                onClick={handleLaunchCampaign}
                className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/20"
              >
                ✓ Confirm &amp; Launch
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
