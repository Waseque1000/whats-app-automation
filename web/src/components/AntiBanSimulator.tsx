"use client";

import { useState } from "react";
import { Shield, Sparkles, Send, CheckCircle2, AlertCircle, RefreshCw, CheckCheck } from "lucide-react";
import { applySpintaxDynamic } from "../lib/spintax";

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
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold mb-4 shadow-sm">
          <Shield className="w-3.5 h-3.5 text-emerald-600" />
          <span>Interactive Anti-Ban Engine Simulator</span>
        </div>
        <h2 className="text-3xl sm:text-5xl font-black text-slate-900 tracking-tight leading-tight">
          Experience the <span className="text-gradient">Anti-Restriction Rotation</span> Live
        </h2>
        <p className="mt-4 text-slate-600 text-sm sm:text-base leading-relaxed">
          Blasting the exact same message to 50+ numbers triggers WhatsApp spam flags. WhatsPulse rotates 3 to 5 message variations sequentially with dynamic Spintax, simulating organic manual chats.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        {/* Left Studio Editor */}
        <div className="lg:col-span-6 bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xl flex flex-col justify-between">
          <div className="space-y-5">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-200 font-bold">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="font-bold text-sm sm:text-base text-slate-900">Multi-SMS Variation Studio</h3>
                  <p className="text-[11px] text-slate-500">Sequential round-robin pattern active</p>
                </div>
              </div>
              <span className="text-xs px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-bold border border-emerald-200 font-mono">
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
                      ? "bg-emerald-600 text-white shadow-md shadow-emerald-600/20"
                      : "bg-slate-100 text-slate-600 hover:text-slate-900 hover:bg-slate-200 border border-slate-200"
                  }`}
                >
                  SMS #{idx + 1}
                </button>
              ))}
            </div>

            {/* Active Variant Editor */}
            <div className="space-y-3">
              <div className="flex items-center justify-between text-xs text-slate-500">
                <span>Editing: <strong className="text-slate-900">Design #{activeTab + 1}</strong></span>
                <span className="text-[11px] text-emerald-600 font-mono font-semibold">Supports Spintax &bull; &#123;Hello|Hi&#125;</span>
              </div>
              <textarea
                rows={4}
                value={variants[activeTab]}
                onChange={(e) => {
                  const updated = [...variants];
                  updated[activeTab] = e.target.value;
                  setVariants(updated);
                }}
                className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-xs sm:text-sm text-slate-900 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors resize-none font-sans leading-relaxed shadow-sm"
              />
              
              {/* Chips */}
              <div className="flex flex-wrap gap-2 text-xs">
                <span className="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-medium">
                  Variable: <code className="text-emerald-700 font-bold">&#123;name&#125;</code>
                </span>
                <span className="px-2.5 py-1 rounded-lg bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-medium">
                  Variable: <code className="text-emerald-700 font-bold">&#123;roll&#125;</code>
                </span>
                <span className="px-2.5 py-1 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200 text-[11px] font-medium">
                  Spintax: <code className="text-emerald-700 font-bold">&#123;হ্যালো|প্রিয়&#125;</code>
                </span>
              </div>
            </div>
          </div>

          {/* Action Trigger */}
          <div className="mt-6 pt-5 border-t border-slate-100 flex items-center gap-3">
            <button
              onClick={handleNextDispatch}
              className="flex-1 flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-emerald-600 hover:bg-emerald-500 text-white font-black text-xs sm:text-sm shadow-lg shadow-emerald-600/25 transition-all hover:scale-[1.01] active:scale-[0.98]"
            >
              <Send className="w-4 h-4 fill-white" />
              <span>Simulate Next Dispatch</span>
            </button>
            <button
              onClick={handleReset}
              className="p-3.5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-600 hover:text-slate-900 transition-colors border border-slate-200"
              title="Reset feed"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Right WhatsApp Mobile Screen Mockup (Authentic Light Theme) */}
        <div className="lg:col-span-6 bg-[#efeae2] rounded-3xl border border-slate-300 shadow-xl flex flex-col justify-between overflow-hidden relative min-h-[460px]">
          {/* WhatsApp Header Bar */}
          <div className="bg-[#008069] px-5 py-3.5 flex items-center justify-between text-white z-10 shadow-sm">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full bg-white/20 border border-white/40 flex items-center justify-center text-white font-bold text-xs">
                WP
              </div>
              <div>
                <h4 className="text-xs font-bold leading-none text-white">WhatsApp Student Dispatch</h4>
                <span className="text-[10px] text-emerald-100 font-medium">● Connected (Cloud Session)</span>
              </div>
            </div>
            <span className="text-[11px] font-mono text-emerald-100">
              {currentIndex} Dispatched
            </span>
          </div>

          {/* Chat Messages Stream */}
          <div className="p-4 sm:p-6 space-y-4 flex-1 overflow-y-auto">
            {history.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8 space-y-3">
                <div className="w-12 h-12 rounded-2xl bg-white/80 border border-slate-300/80 flex items-center justify-center text-emerald-600 shadow-sm">
                  <Send className="w-5 h-5" />
                </div>
                <p className="text-xs text-slate-600 max-w-xs font-medium">
                  Click <strong className="text-emerald-700">&ldquo;Simulate Next Dispatch&rdquo;</strong> to watch how different students receive rotating designs and how non-WhatsApp numbers auto-skip!
                </p>
              </div>
            ) : (
              history.map((item, idx) => (
                <div key={idx} className="space-y-1 animate-in fade-in slide-in-from-bottom-2">
                  <div className="flex items-center justify-between px-1 text-[11px] text-slate-600">
                    <span className="font-semibold text-slate-800">To: {item.student.name} ({item.student.phone})</span>
                    <span className={`px-1.5 py-0.2 rounded text-[10px] font-bold ${
                      item.status === 'skipped'
                        ? 'bg-amber-100 text-amber-800 border border-amber-300'
                        : 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                    }`}>
                      {item.smsType}
                    </span>
                  </div>

                  {item.status === 'skipped' ? (
                    <div className="p-3 rounded-2xl bg-amber-50 border border-amber-200 text-xs text-amber-800 flex items-center gap-2 shadow-sm">
                      <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
                      <span>{item.message} &bull; <strong>Auto-Advanced</strong></span>
                    </div>
                  ) : (
                    <div className="flex justify-end">
                      <div className="max-w-[85%] bg-[#d9fdd3] text-slate-900 p-3.5 rounded-2xl rounded-tr-none shadow-sm space-y-1 border border-emerald-200/50">
                        <p className="text-xs sm:text-[13px] leading-relaxed">
                          {item.message}
                        </p>
                        <div className="flex items-center justify-end gap-1 text-[10px] text-slate-500 font-medium">
                          <span>{item.time}</span>
                          <CheckCheck className="w-3.5 h-3.5 text-blue-500" />
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          {/* Footer bar */}
          <div className="bg-[#f0f2f5] px-4 py-2.5 flex items-center justify-between text-[11px] text-slate-600 border-t border-slate-300">
            <span className="flex items-center gap-1.5 text-emerald-700 font-semibold">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Anti-Spam Algorithmic Protection Active</span>
            </span>
            <span className="text-slate-600 font-mono font-medium">0% Ban Rate</span>
          </div>
        </div>
      </div>
    </section>
  );
}
