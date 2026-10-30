"use client";

import { useState } from "react";
import { Shield, Sparkles, Send, CheckCircle2, AlertCircle, RefreshCw, Zap } from "lucide-react";
import { applySpintax, applySpintaxDynamic } from "../lib/spintax";

export function AntiBanSimulator() {
  const [activeTab, setActiveTab] = useState(0);
  const [variants, setVariants] = useState<string[]>([
    "{হ্যালো|প্রিয়} {name}! তোমার আসন্ন ক্লাসের অ্যাসাইনমেন্ট রবিবার জমা দাও।",
    "আসসালামু আলাইকুম {name}, আশা করি ভালো আছো। মনে করিয়ে দিচ্ছি যে আগামী সোমবার ক্লাস টেস্ট।",
    "{Hey|Hello} {name}! অনুগ্রহ করে তোমার রোল {roll}-এর হোমওয়ার্ক কমপ্লিট করে ফেলো।"
  ]);

  const students = [
    { name: "Tanvir Ahmed", phone: "+8801712345671", roll: "101", hasWhatsApp: true },
    { name: "Sadia Rahman", phone: "+8801812345672", roll: "102", hasWhatsApp: true },
    { name: "Farhan Hossain (No WhatsApp)", phone: "+8801912345673", roll: "103", hasWhatsApp: false },
    { name: "Nusrat Jahan", phone: "+8801612345674", roll: "104", hasWhatsApp: true },
    { name: "Shreya Barai", phone: "+8801917820336", roll: "105", hasWhatsApp: true },
  ];

  const [currentIndex, setCurrentIndex] = useState(0);
  const [history, setHistory] = useState<Array<{
    student: typeof students[0];
    smsType: string;
    message: string;
    status: 'sent' | 'skipped';
  }>>([]);

  const handleNextDispatch = () => {
    const student = students[currentIndex % students.length];
    const variantIndex = currentIndex % variants.length;
    const rawTemplate = variants[variantIndex];

    let rendered = rawTemplate
      .replace(/\{name\}/gi, student.name.split(" ")[0])
      .replace(/\{roll\}/gi, student.roll);
    rendered = applySpintaxDynamic(rendered);

    const isSkipped = !student.hasWhatsApp;

    setHistory((prev) => [
      {
        student,
        smsType: `SMS #${variantIndex + 1}`,
        message: isSkipped ? "Auto-dismissed WhatsApp Web error popup ('Phone number shared via url is invalid'). Zero delay skip." : rendered,
        status: isSkipped ? 'skipped' : 'sent',
      },
      ...prev.slice(0, 4),
    ]);

    setCurrentIndex((prev) => prev + 1);
  };

  const handleReset = () => {
    setHistory([]);
    setCurrentIndex(0);
  };

  return (
    <section id="simulator" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto">
      <div className="text-center max-w-3xl mx-auto mb-12">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-4">
          <Shield className="w-3.5 h-3.5" />
          <span>Interactive Live Demo</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
          See How the <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">Anti-Restriction Rotation</span> Protects You
        </h2>
        <p className="mt-3 text-slate-400 text-sm sm:text-base leading-relaxed">
          Sending the exact same message to 50+ numbers triggers WhatsApp spam flags. WhatsPulse rotates 3 to 5 message designs sequentially and parses Spintax dynamically.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Studio Editor */}
        <div className="lg:col-span-6 glass-panel rounded-2xl p-6 border border-slate-800 shadow-2xl">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-base text-white flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-emerald-400" />
              <span>Multi-SMS Variation Studio</span>
            </h3>
            <span className="text-xs px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              3 Active Designs
            </span>
          </div>

          {/* Variant Tabs */}
          <div className="flex space-x-2 border-b border-slate-800 pb-2 mb-4 overflow-x-auto">
            {variants.map((_, idx) => (
              <button
                key={idx}
                onClick={() => setActiveTab(idx)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                  activeTab === idx
                    ? "bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20"
                    : "bg-slate-900 text-slate-400 hover:text-white hover:bg-slate-800"
                }`}
              >
                SMS #{idx + 1}
              </button>
            ))}
          </div>

          {/* Active Variant Editor */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Editing: <strong className="text-white">Design #{activeTab + 1}</strong></span>
              <span className="text-[11px] text-emerald-400">Supports Spintax &bull; &#123;Hello|Hi&#125;</span>
            </div>
            <textarea
              rows={4}
              value={variants[activeTab]}
              onChange={(e) => {
                const updated = [...variants];
                updated[activeTab] = e.target.value;
                setVariants(updated);
              }}
              className="w-full bg-slate-950/80 border border-slate-850 rounded-xl p-3.5 text-sm text-slate-100 focus:outline-none focus:border-emerald-500 transition-colors resize-none font-mono"
            />
            
            {/* Chips */}
            <div className="flex flex-wrap gap-2 text-xs">
              <span className="px-2 py-1 rounded bg-slate-800/80 text-slate-300 border border-slate-700">
                Tag: &#123;name&#125;
              </span>
              <span className="px-2 py-1 rounded bg-slate-800/80 text-slate-300 border border-slate-700">
                Tag: &#123;roll&#125;
              </span>
              <span className="px-2 py-1 rounded bg-slate-800/80 text-emerald-400 border border-emerald-500/30">
                Spintax: &#123;হ্যালো|প্রিয়&#125;
              </span>
            </div>
          </div>

          {/* Action Trigger */}
          <div className="mt-6 pt-4 border-t border-slate-800/80 flex items-center justify-between gap-3">
            <button
              onClick={handleNextDispatch}
              className="flex-1 flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/25 transition-all hover:scale-[1.01] active:scale-[0.98]"
            >
              <Send className="w-4 h-4 fill-slate-950" />
              <span>Simulate Next Dispatch</span>
            </button>
            <button
              onClick={handleReset}
              className="px-3 py-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-white transition-colors border border-slate-800"
              title="Reset simulator"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Right Live Dispatch Feed */}
        <div className="lg:col-span-6 glass-panel rounded-2xl p-6 border border-slate-800 shadow-2xl flex flex-col justify-between min-h-[420px]">
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-base text-white flex items-center gap-2">
                <Zap className="w-4 h-4 text-amber-400" />
                <span>Live Recipient Dispatch Feed</span>
              </h3>
              <span className="text-xs text-slate-400 font-mono">
                Queue Total: {currentIndex} sent/skipped
              </span>
            </div>

            <div className="space-y-3">
              {history.length === 0 ? (
                <div className="p-8 text-center text-slate-500 text-sm border border-dashed border-slate-850 rounded-xl my-4">
                  <p>Click <strong className="text-emerald-400">&quot;Simulate Next Dispatch&quot;</strong> on the left to watch sequential SMS rotation and automatic non-WhatsApp skip handling.</p>
                </div>
              ) : (
                history.map((item, idx) => (
                  <div
                    key={idx}
                    className={`p-3.5 rounded-xl border transition-all animate-in fade-in slide-in-from-top-2 ${
                      item.status === 'skipped'
                        ? 'bg-amber-950/20 border-amber-500/30'
                        : 'bg-slate-900/80 border-slate-800'
                    }`}
                  >
                    <div className="flex items-center justify-between text-xs mb-1.5">
                      <span className="font-semibold text-slate-200">
                        {item.student.name} ({item.student.phone})
                      </span>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          item.status === 'skipped'
                            ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                            : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                        }`}>
                          {item.smsType}
                        </span>
                        {item.status === 'skipped' ? (
                          <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-amber-400">
                            <AlertCircle className="w-3.5 h-3.5" /> Auto-Skipped
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-emerald-400">
                            <CheckCircle2 className="w-3.5 h-3.5" /> Delivered
                          </span>
                        )}
                      </div>
                    </div>
                    <p className={`text-xs ${item.status === 'skipped' ? 'text-amber-200/80 italic' : 'text-slate-300'}`}>
                      &ldquo;{item.message}&rdquo;
                    </p>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-850 flex items-center justify-between text-xs text-slate-400">
            <span className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Round-Robin Pattern: 1 ➔ 2 ➔ 3 ➔ 1 ➔ 2
            </span>
            <span className="text-[11px] text-slate-500">
              Zero Meta Conversation Fees
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
