"use client";

import { useState } from "react";
import { Shield, Sparkles, Send, CheckCircle2, AlertCircle, RefreshCw, Zap, CheckCheck } from "lucide-react";
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
    time: string;
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
    const now = new Date();
    const timeStr = `${now.getHours() % 12 || 12}:${String(now.getMinutes()).padStart(2, '0')} ${now.getHours() >= 12 ? 'PM' : 'AM'}`;

    setHistory((prev) => [
      {
        student,
        smsType: `SMS #${variantIndex + 1}`,
        message: isSkipped ? "Auto-dismissed invalid phone alert (Skipped with zero stall)" : rendered,
        status: isSkipped ? 'skipped' : 'sent',
        time: timeStr,
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
    <section id="simulator" className="py-20 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto relative">
      <div className="text-center max-w-3xl mx-auto mb-14">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold mb-4 shadow-inner">
          <Shield className="w-3.5 h-3.5" />
          <span>Interactive Anti-Ban Engine Simulator</span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-black text-white tracking-tight leading-tight">
          Experience the <span className="text-gradient">Anti-Restriction Rotation</span> Live
        </h2>
        <p className="mt-4 text-slate-400 text-sm sm:text-base leading-relaxed">
          Blasting the exact same message to 50+ numbers triggers WhatsApp spam flags. WhatsPulse rotates 3 to 5 message variations sequentially with dynamic Spintax, simulating organic manual chats.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        {/* Left Studio Editor */}
        <div className="lg:col-span-6 glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 shadow-2xl flex flex-col justify-between">
          <div className="space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/30">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="font-bold text-sm sm:text-base text-white">Multi-SMS Variation Studio</h3>
                  <p className="text-[11px] text-slate-400">Sequential round-robin pattern active</p>
                </div>
              </div>
              <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-300 font-bold border border-emerald-500/20 font-mono">
                3 Variants
              </span>
            </div>

            {/* Variant Tabs */}
            <div className="flex space-x-2 pb-1 overflow-x-auto">
              {variants.map((_, idx) => (
                <button
                  key={idx}
                  onClick={() => setActiveTab(idx)}
                  className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                    activeTab === idx
                      ? "bg-gradient-to-r from-emerald-500 to-teal-400 text-slate-950 shadow-md shadow-emerald-500/20 scale-105"
                      : "bg-slate-900/80 text-slate-400 hover:text-white hover:bg-slate-850 border border-slate-800"
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
                <span className="text-[11px] text-emerald-400 font-mono">Supports Spintax &bull; &#123;Hello|Hi&#125;</span>
              </div>
              <textarea
                rows={4}
                value={variants[activeTab]}
                onChange={(e) => {
                  const updated = [...variants];
                  updated[activeTab] = e.target.value;
                  setVariants(updated);
                }}
                className="w-full bg-[#070b14] border border-slate-800 rounded-2xl p-4 text-xs sm:text-sm text-slate-100 focus:outline-none focus:border-emerald-500 transition-colors resize-none font-sans leading-relaxed shadow-inner"
              />
              
              {/* Chips */}
              <div className="flex flex-wrap gap-2 text-xs">
                <span className="px-2.5 py-1 rounded-lg bg-slate-900 text-slate-300 border border-slate-800 text-[11px]">
                  Variable: <code className="text-emerald-400">&#123;name&#125;</code>
                </span>
                <span className="px-2.5 py-1 rounded-lg bg-slate-900 text-slate-300 border border-slate-800 text-[11px]">
                  Variable: <code className="text-emerald-400">&#123;roll&#125;</code>
                </span>
                <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/25 text-[11px]">
                  Spintax: <code className="text-emerald-300">&#123;হ্যালো|প্রিয়&#125;</code>
                </span>
              </div>
            </div>
          </div>

          {/* Action Trigger */}
          <div className="mt-6 pt-5 border-t border-slate-800/80 flex items-center gap-3">
            <button
              onClick={handleNextDispatch}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 hover:opacity-95 text-slate-950 font-black text-xs sm:text-sm shadow-xl shadow-emerald-500/25 transition-all hover:scale-[1.01] active:scale-[0.98]"
            >
              <Send className="w-4 h-4 fill-slate-950" />
              <span>Simulate Next Dispatch</span>
            </button>
            <button
              onClick={handleReset}
              className="p-3.5 rounded-2xl bg-slate-900 hover:bg-slate-850 text-slate-400 hover:text-white transition-colors border border-slate-800"
              title="Reset feed"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Right WhatsApp Mobile Screen Mockup */}
        <div className="lg:col-span-6 bg-[#0b141a] rounded-3xl border border-slate-800 shadow-2xl flex flex-col justify-between overflow-hidden relative min-h-[460px]">
          {/* WhatsApp Header Bar */}
          <div className="bg-[#1f2c34] px-5 py-3.5 flex items-center justify-between border-b border-[#2a3942] z-10">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-emerald-600/30 border border-emerald-500/40 flex items-center justify-center text-emerald-400 font-bold text-xs">
                WP
              </div>
              <div>
                <h4 className="text-xs font-bold text-white leading-none">WhatsApp Student Dispatch</h4>
                <span className="text-[10px] text-emerald-400 font-medium">● Connected (Cloud Session)</span>
              </div>
            </div>
            <span className="text-[11px] font-mono text-slate-400">
              {currentIndex} Dispatched
            </span>
          </div>

          {/* Chat Messages Stream */}
          <div className="p-4 sm:p-6 space-y-4 flex-1 overflow-y-auto">
            {history.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-slate-800/60 border border-slate-700/60 flex items-center justify-center text-emerald-400">
                  <Send className="w-5 h-5" />
                </div>
                <p className="text-xs text-slate-400 max-w-xs">
                  Click <strong className="text-emerald-400">&ldquo;Simulate Next Dispatch&rdquo;</strong> to watch how different students receive rotating designs and how non-WhatsApp numbers auto-skip!
                </p>
              </div>
            ) : (
              history.map((item, idx) => (
                <div key={idx} className="space-y-1 animate-in fade-in slide-in-from-bottom-2">
                  <div className="flex items-center justify-between px-1 text-[11px] text-slate-400">
                    <span className="font-medium text-slate-300">To: {item.student.name} ({item.student.phone})</span>
                    <span className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                      item.status === 'skipped'
                        ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                        : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                    }`}>
                      {item.smsType}
                    </span>
                  </div>

                  {item.status === 'skipped' ? (
                    <div className="p-3 rounded-2xl bg-amber-950/40 border border-amber-500/30 text-xs text-amber-200 flex items-center gap-2">
                      <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0" />
                      <span>{item.message} &bull; <strong>Auto-Advanced</strong></span>
                    </div>
                  ) : (
                    <div className="flex justify-end">
                      <div className="max-w-[85%] bg-[#005c4b] text-white p-3 rounded-2xl rounded-tr-none shadow-md space-y-1">
                        <p className="text-xs sm:text-[13px] leading-relaxed">
                          {item.message}
                        </p>
                        <div className="flex items-center justify-end gap-1 text-[10px] text-emerald-200/80">
                          <span>{item.time}</span>
                          <CheckCheck className="w-3.5 h-3.5 text-cyan-300" />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          {/* Footer bar */}
          <div className="bg-[#1f2c34] px-4 py-2.5 flex items-center justify-between text-[11px] text-slate-400 border-t border-[#2a3942]">
            <span className="flex items-center gap-1.5 text-emerald-400 font-semibold">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Anti-Spam Algorithmic Protection Active</span>
            </span>
            <span className="text-slate-400 font-mono">0% Ban Rate</span>
          </div>
        </div>
      </div>
    </section>
  );
}
