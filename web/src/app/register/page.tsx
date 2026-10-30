"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import {
  MessageSquare,
  ShieldCheck,
  Mail,
  Lock,
  User,
  Building,
  ArrowRight,
  AlertCircle,
  CheckCircle2,
  Sparkles
} from "lucide-react";
import { createClient } from "@/lib/supabase/client";

export default function RegisterPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [organization, setOrganization] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [selectedPlan, setSelectedPlan] = useState<"starter" | "pro" | "agency">("pro");
  const [agreeTerms, setAgreeTerms] = useState(true);

  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const supabase = createClient();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!agreeTerms) {
      setErrorMsg("Please agree to the Terms of Service.");
      return;
    }

    try {
      setIsLoading(true);
      setSuccessMsg("Direct access enabled! Entering workspace...");
      setTimeout(() => {
        router.push("/app");
      }, 300);
      return;
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to create account";
      setErrorMsg(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] text-slate-900 flex flex-col justify-center items-center px-4 py-12 relative overflow-hidden selection:bg-emerald-500 selection:text-white">
      {/* Brand Header */}
      <div className="mb-6 text-center space-y-2 relative z-10">
        <Link href="/" className="inline-flex items-center gap-2.5 mb-1 group">
          <div className="w-10 h-10 rounded-xl bg-emerald-600 flex items-center justify-center text-white shadow-md shadow-emerald-600/20 group-hover:scale-105 transition-transform">
            <MessageSquare className="w-5 h-5 fill-white text-white" />
          </div>
          <span className="font-extrabold text-2xl tracking-tight text-slate-900">
            WhatsPulse <span className="text-xs uppercase font-bold px-2 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">SaaS</span>
          </span>
        </Link>
        <h1 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight">
          Create Your Academy / Business Account
        </h1>
        <p className="text-xs text-slate-500 max-w-sm">
          Start broadcasting with multi-variant anti-restriction rotation and automatic invalid number skipping.
        </p>
      </div>

      {/* Main Glassmorphic Auth Card */}
      <div className="w-full max-w-lg bg-white rounded-3xl p-8 border border-slate-200 shadow-xl relative z-10 space-y-6">
        <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-200 text-xs space-y-2 text-slate-700">
          <div className="flex items-center gap-1.5 font-bold text-emerald-800">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>Direct Access Mode (Registration Inactive)</span>
          </div>
          <p className="text-[11px] text-slate-600 leading-relaxed font-medium">
            Registration is currently bypassed for testing. You can jump directly into your workspace.
          </p>
          <Link
            href="/app"
            className="w-full flex items-center justify-center gap-1.5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow transition-all"
          >
            <span>Enter Dashboard Directly</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Error Alert */}
        {errorMsg && (
          <div className="p-3.5 rounded-xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-600 flex-shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Success Alert */}
        {successMsg && (
          <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-700 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            <div className="space-y-1.5">
              <label className="text-slate-700 font-bold block">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  placeholder="Waseque Ahmed"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-3.5 py-2.5 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-700 font-bold block">Academy / Business Name</label>
              <div className="relative">
                <Building className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  placeholder="Durber Coaching"
                  value={organization}
                  onChange={(e) => setOrganization(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-3.5 py-2.5 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors"
                />
              </div>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-slate-700 font-bold block">Work Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                placeholder="waseque@durber.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-slate-700 font-bold block">Create Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                minLength={6}
                placeholder="Minimum 6 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-slate-900 placeholder-slate-400 focus:outline-none focus:border-emerald-500 focus:bg-white transition-colors font-mono"
              />
            </div>
          </div>

          {/* Select Tier Plan */}
          <div className="space-y-2 pt-1">
            <label className="text-slate-700 font-bold block">Selected SaaS Tier</label>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setSelectedPlan("starter")}
                className={`p-3 rounded-2xl border text-left transition-all ${
                  selectedPlan === "starter"
                    ? "bg-emerald-50 border-emerald-500 text-slate-900 shadow-sm"
                    : "bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900"
                }`}
              >
                <div className="font-bold text-xs text-slate-900">Starter</div>
                <div className="text-[11px] text-emerald-700 font-mono font-bold mt-0.5">$19/mo</div>
                <div className="text-[10px] text-slate-500 mt-1">3k msgs</div>
              </button>

              <button
                type="button"
                onClick={() => setSelectedPlan("pro")}
                className={`p-3 rounded-2xl border text-left relative transition-all ${
                  selectedPlan === "pro"
                    ? "bg-emerald-50 border-emerald-500 text-slate-900 shadow-sm"
                    : "bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900"
                }`}
              >
                <span className="absolute -top-2 right-2 px-1.5 py-0.2 rounded bg-emerald-600 text-white text-[9px] font-extrabold uppercase">
                  Popular
                </span>
                <div className="font-bold text-xs text-slate-900">Pro Academy</div>
                <div className="text-[11px] text-emerald-700 font-mono font-bold mt-0.5">$49/mo</div>
                <div className="text-[10px] text-slate-500 mt-1">25k msgs</div>
              </button>

              <button
                type="button"
                onClick={() => setSelectedPlan("agency")}
                className={`p-3 rounded-2xl border text-left transition-all ${
                  selectedPlan === "agency"
                    ? "bg-emerald-50 border-emerald-500 text-slate-900 shadow-sm"
                    : "bg-slate-50 border-slate-200 text-slate-600 hover:text-slate-900"
                }`}
              >
                <div className="font-bold text-xs text-slate-900">Agency</div>
                <div className="text-[11px] text-emerald-700 font-mono font-bold mt-0.5">$99/mo</div>
                <div className="text-[10px] text-slate-500 mt-1">100k msgs</div>
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs shadow-md shadow-emerald-600/25 transition-all flex items-center justify-center gap-2 hover:scale-[1.01] active:scale-[0.98]"
          >
            <span>{isLoading ? "Entering Dashboard..." : "Enter Workspace (Direct Access)"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>
      </div>

      <div className="mt-8 flex items-center gap-2 text-xs text-slate-500 font-medium">
        <ShieldCheck className="w-4 h-4 text-emerald-600" />
        <span>Stored securely in your isolated Supabase multi-tenant database</span>
      </div>
    </div>
  );
}
