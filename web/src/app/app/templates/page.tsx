"use client";

import { useState } from "react";
import { Plus, Sparkles, Trash2 } from "lucide-react";
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
          <h1 className="text-2xl font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
            <span>Message Templates Library</span>
            <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
              Anti-Restriction Ready
            </span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Store multi-variant message templates that automatically alternate between 2 to 5 designs during campaigns.
          </p>
        </div>

        <button
          onClick={() => setModalOpen(true)}
          className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/20 transition-all self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>+ Create Multi-SMS Template</span>
        </button>
      </div>

      {/* Templates Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {templates.map((tpl) => (
          <div key={tpl.id} className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4 hover:shadow-md transition-all">
            <div className="flex items-start justify-between">
              <div>
                <span className="text-[10px] uppercase font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700 border border-slate-200">
                  {tpl.category}
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-2">{tpl.title}</h3>
                <span className="text-[11px] text-slate-400 font-medium">Last updated: {tpl.updatedAt}</span>
              </div>

              <div className="flex items-center gap-1">
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[10px] font-bold">
                  {tpl.variants.length} Designs
                </span>
                <button
                  onClick={() => setTemplates(templates.filter(t => t.id !== tpl.id))}
                  className="p-1.5 text-slate-400 hover:text-red-500 transition-colors ml-1"
                  title="Delete template"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {/* Variants Accordion / Preview */}
            <div className="space-y-2 pt-1">
              {tpl.variants.map((v, i) => (
                <div key={i} className="p-3 rounded-2xl bg-slate-50 border border-slate-200 text-xs">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-emerald-700 text-[10px] uppercase tracking-wider">SMS #{i + 1}</span>
                    <span className="text-[10px] text-slate-400 font-medium">{v.length} chars</span>
                  </div>
                  <p className="text-slate-700 font-sans leading-relaxed text-[11px] line-clamp-2">
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
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-lg rounded-3xl p-6 border border-slate-200 shadow-2xl space-y-4">
            <h3 className="font-bold text-base text-slate-900 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-emerald-600" />
              <span>Create Multi-Variation Template</span>
            </h3>

            <form onSubmit={handleAddTemplate} className="space-y-4 text-xs">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-600 font-bold block mb-1">Template Title</label>
                  <input
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-emerald-500 focus:bg-white"
                    placeholder="e.g. Monthly Exam Reminder"
                  />
                </div>
                <div>
                  <label className="text-slate-600 font-bold block mb-1">Category</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-slate-900 focus:outline-none focus:border-emerald-500 focus:bg-white font-medium"
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
                  <span className="text-slate-600 font-bold">Design Variations:</span>
                  <button
                    type="button"
                    onClick={() => {
                      setVariants([...variants, `Variant #${variants.length + 1}: Hello {name}, please note...`]);
                      setActiveTab(variants.length);
                    }}
                    className="text-emerald-700 font-bold hover:underline text-[11px]"
                  >
                    + Add Another Variant
                  </button>
                </div>

                <div className="flex space-x-1.5 border-b border-slate-100 pb-2">
                  {variants.map((_, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => setActiveTab(idx)}
                      className={`px-3 py-1 rounded-xl text-xs font-bold ${
                        activeTab === idx ? "bg-emerald-600 text-white shadow-xs" : "bg-slate-100 text-slate-600"
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
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-3 text-xs text-slate-900 focus:outline-none focus:border-emerald-500 focus:bg-white"
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-100 text-slate-600 hover:text-slate-900 font-bold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-emerald-600 text-white font-bold shadow-sm"
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
