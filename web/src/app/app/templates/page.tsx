"use client";

import { useState } from "react";
import { FileText, Plus, Sparkles, Trash2, Copy, Check, ShieldCheck } from "lucide-react";
import { INITIAL_TEMPLATES } from "../../../lib/mock-data";
import { Template } from "../../../types";

export default function TemplatesPage() {
  const [templates, setTemplates] = useState<Template[]>(INITIAL_TEMPLATES);
  const [modalOpen, setModalOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [category, setCategory] = useState("Academic");
  const [variants, setVariants] = useState<string[]>([
    "Variant 1: Hello {name}, this is an important message from our institute.",
    "Variant 2: Greetings {name}, please check your class assignments for this week."
  ]);
  const [activeTab, setActiveTab] = useState(0);

  const handleAddTemplate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!title || variants.length === 0) return;

    const newTpl: Template = {
      id: Date.now(),
      title,
      category,
      variants,
      updatedAt: new Date().toISOString().slice(0, 10)
    };

    setTemplates([newTpl, ...templates]);
    setModalOpen(false);
    setTitle("");
    setVariants([
      "Variant 1: Hello {name}, this is an important message.",
      "Variant 2: Greetings {name}, check your portal updates."
    ]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <span>Message Templates Library</span>
            <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              Anti-Restriction Ready
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Store multi-variant message templates that automatically alternate between 2 to 5 designs during campaigns.
          </p>
        </div>

        <button
          onClick={() => setModalOpen(true)}
          className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>+ Create Multi-SMS Template</span>
        </button>
      </div>

      {/* Templates Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {templates.map((tpl) => (
          <div key={tpl.id} className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4 hover:border-slate-700 transition-all">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800">
                  {tpl.category}
                </span>
                <h3 className="text-base font-bold text-white mt-1.5">{tpl.title}</h3>
                <span className="text-[11px] text-slate-500">Last updated: {tpl.updatedAt}</span>
              </div>

              <div className="flex items-center gap-1">
                <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] font-bold">
                  {tpl.variants.length} Designs
                </span>
                <button
                  onClick={() => setTemplates(templates.filter(t => t.id !== tpl.id))}
                  className="p-1.5 text-slate-500 hover:text-red-400 transition-colors ml-1"
                  title="Delete template"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Variants Accordion / Preview */}
            <div className="space-y-2 pt-1">
              {tpl.variants.map((v, i) => (
                <div key={i} className="p-3 rounded-xl bg-slate-950/70 border border-slate-850 text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-semibold text-emerald-400 text-[10px] uppercase tracking-wider">SMS #{i + 1}</span>
                    <span className="text-[10px] text-slate-500">{v.length} chars</span>
                  </div>
                  <p className="text-slate-300 font-sans leading-relaxed text-[11px] line-clamp-2">
                    {v}
                  </p>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Create Template Modal */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel w-full max-w-lg rounded-2xl p-6 border border-slate-800 shadow-2xl space-y-4">
            <h3 className="font-bold text-base text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <span>Create Multi-Variation Template</span>
            </h3>

            <form onSubmit={handleAddTemplate} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1">Template Title</label>
                  <input
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                    placeholder="e.g. Monthly Exam Reminder"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1">Category</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                  >
                    <option value="Academic">Academic Notice</option>
                    <option value="Finance">Tuition &amp; Fees</option>
                    <option value="Onboarding">Admission &amp; Welcome</option>
                    <option value="General">General Broadcast</option>
                  </select>
                </div>
              </div>

              {/* Variant Tabs */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Design Variations:</span>
                  <button
                    type="button"
                    onClick={() => {
                      setVariants([...variants, `Variant #${variants.length + 1}: Hello {name}, please note...`]);
                      setActiveTab(variants.length);
                    }}
                    className="text-emerald-400 hover:underline text-[11px]"
                  >
                    + Add Another Variant
                  </button>
                </div>

                <div className="flex space-x-1.5 border-b border-slate-800 pb-2">
                  {variants.map((_, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setActiveTab(idx)}
                      className={`px-3 py-1 rounded-lg text-xs font-semibold ${
                        activeTab === idx ? "bg-emerald-500 text-slate-950 font-bold" : "bg-slate-900 text-slate-400"
                      }`}
                    >
                      SMS #{idx + 1}
                    </button>
                  ))}
                </div>

                <textarea
                  rows={4}
                  value={variants[activeTab]}
                  onChange={(e) => {
                    const updated = [...variants];
                    updated[activeTab] = e.target.value;
                    setVariants(updated);
                  }}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-900 text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-emerald-500 text-slate-950 font-bold"
                >
                  Save Template
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

