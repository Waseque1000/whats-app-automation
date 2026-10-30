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
  Sparkles,
  Check
} from "lucide-react";
import { createClient, isSupabaseConfigured } from "@/lib/supabase/client";

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
  const configured = isSupabaseConfigured();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!agreeTerms) {
      setErrorMsg("Please agree to the Terms of Service.");
      return;
    }

    setIsLoading(true);
    setErrorMsg("");
    setSuccessMsg("");

    try {
      if (!configured) {
        // Fallback for preview / demo mode
        setSuccessMsg("Account created in Preview Mode! Launching your workspace...");
        setTimeout(() => {
          router.push("/app");
        }, 800);
        return;
      }

      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: fullName,
            organization: organization,
            plan: selectedPlan,
          },
          emailRedirectTo: `${window.location.origin}/auth/callback`,
        },
      });

      if (error) {
        setErrorMsg(error.message);
      } else if (data.session) {
        setSuccessMsg("Account registered successfully! Redirecting...");
        setTimeout(() => router.push("/app"), 600);
      } else {
        setSuccessMsg("Registration successful! Please check your email to confirm your account.");
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to create account";
      setErrorMsg(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#060911] text-slate-100 flex flex-col justify-center items-center px-4 py-12 relative overflow-hidden selection:bg-emerald-500 selection:text-slate-950">
      {/* Ambient background glows */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[700px] h-[400px] bg-emerald-500/12 rounded-full blur-[150px] pointer-events-none" />
      <div className="absolute bottom-10 left-10 w-[350px] h-[250px] bg-cyan-500/10 rounded-full blur-[130px] pointer-events-none" />

      {/* Brand Header */}
      <div className="mb-6 text-center space-y-2 relative z-10">
        <Link href="/" className="inline-flex items-center gap-2.5 mb-1 group">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center text-slate-950 shadow-lg shadow-emerald-500/25 group-hover:scale-105 transition-transform">
            <MessageSquare className="w-5 h-5 fill-slate-950 text-slate-950" />
          </div>
          <span className="font-extrabold text-2xl tracking-tight text-white">
            WhatsPulse <span className="text-xs uppercase font-bold px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-400 border border-emerald-500/25">SaaS</span>
          </span>
        </Link>
        <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
          Create Your Academy / Business Account
        </h1>
        <p className="text-xs text-slate-400 max-w-sm">
          Start broadcasting with multi-variant anti-restriction rotation and automatic invalid number skipping.
        </p>
      </div>

      {/* Main Glassmorphic Auth Card */}
      <div className="w-full max-w-lg glass-panel rounded-3xl p-8 border border-slate-800 shadow-2xl relative z-10 space-y-6">
        {/* Error Alert */}
        {errorMsg && (
          <div className="p-3.5 rounded-xl bg-red-950/40 border border-red-500/30 text-xs text-red-300 flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-400 flex-shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* Success Alert */}
        {successMsg && (
          <div className="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-xs text-emerald-300 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        <form onSubmit={handleRegister} className="space-y-4 text-xs">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            <div className="space-y-1.5">
              <label className="text-slate-300 font-medium block">Full Name</label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  placeholder="Waseque Ahmed"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-slate-950/90 border border-slate-800 rounded-xl pl-10 pr-3.5 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition-colors"
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-300 font-medium block">Academy / Business Name</label>
              <div className="relative">
                <Building className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  required
                  placeholder="Durber Coaching"
                  value={organization}
                  onChange={(e) => setOrganization(e.target.value)}
                  className="w-full bg-slate-950/90 border border-slate-800 rounded-xl pl-10 pr-3.5 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition-colors"
                />
              </div>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-slate-300 font-medium block">Work Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="email"
                required
                placeholder="waseque@durber.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-950/90 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition-colors"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-slate-300 font-medium block">Create Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
              <input
                type="password"
                required
                minLength={6}
                placeholder="Minimum 6 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-950/90 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-white placeholder-slate-600 focus:outline-none focus:border-emerald-500 transition-colors font-mono"
              />
            </div>
          </div>

          {/* Select Tier Plan */}
          <div className="space-y-2 pt-1">
            <label className="text-slate-300 font-medium block">Selected SaaS Tier</label>
            <div className="grid grid-cols-3 gap-2">
              <button
                type="button"
                onClick={() => setSelectedPlan("starter")}
                className={`p-3 rounded-xl border text-left transition-all ${
                  selectedPlan === "starter"
                    ? "bg-emerald-950/40 border-emerald-500 text-white shadow-md shadow-emerald-500/10"
                    : "bg-slate-950/80 border-slate-850 text-slate-400 hover:text-white"
                }`}
              >
                <div className="font-bold text-xs">Starter</div>
                <div className="text-[11px] text-emerald-400 font-mono mt-0.5">$19/mo</div>
                <div className="text-[10px] text-slate-500 mt-1">3k msgs</div>
              </button>

              <button
                type="button"
                onClick={() => setSelectedPlan("pro")}
                className={`p-3 rounded-xl border text-left relative transition-all ${
                  selectedPlan === "pro"
                    ? "bg-emerald-950/40 border-emerald-500 text-white shadow-md shadow-emerald-500/10"
                    : "bg-slate-950/80 border-slate-850 text-slate-400 hover:text-white"
                }`}
              >
                <span className="absolute -top-2 right-2 px-1.5 py-0.2 rounded bg-emerald-500 text-slate-950 text-[9px] font-extrabold uppercase">
                  Popular
                </span>
                <div className="font-bold text-xs">Pro Academy</div>
                <div className="text-[11px] text-emerald-400 font-mono mt-0.5">$49/mo</div>
                <div className="text-[10px] text-slate-500 mt-1">25k msgs</div>
              </button>

              <button
                type="button"
                onClick={() => setSelectedPlan("agency")}
                className={`p-3 rounded-xl border text-left transition-all ${
                  selectedPlan === "agency"
                    ? "bg-emerald-950/40 border-emerald-500 text-white shadow-md shadow-emerald-500/10"
                    : "bg-slate-950/80 border-slate-850 text-slate-400 hover:text-white"
                }`}
              >
                <div className="font-bold text-xs">Agency</div>
                <div className="text-[11px] text-emerald-400 font-mono mt-0.5">$99/mo</div>
                <div className="text-[10px] text-slate-500 mt-1">100k msgs</div>
              </button>
            </div>
          </div>

          {/* Consent Checkbox */}
          <label className="flex items-start gap-2.5 pt-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={agreeTerms}
              onChange={(e) => setAgreeTerms(e.target.checked)}
              className="w-4 h-4 mt-0.5 rounded text-emerald-500 accent-emerald-500 bg-slate-900 border-slate-700 cursor-pointer"
            />
            <span className="text-[11px] text-slate-400 leading-snug">
              I agree to the <span className="text-white underline">Terms of Service</span>, Privacy Policy, and WhatsApp anti-spam compliance guidelines.
            </span>
          </label>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full mt-2 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-400 hover:from-emerald-400 hover:to-teal-300 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/25 transition-all flex items-center justify-center gap-2 hover:scale-[1.01] active:scale-[0.98] disabled:opacity-50"
          >
            <span>{isLoading ? "Creating Account..." : "Create Account & Start Free Trial"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Footer Link to Login */}
        <div className="pt-2 text-center text-xs text-slate-400 border-t border-slate-850">
          Already registered?{" "}
          <Link href="/login" className="font-bold text-emerald-400 hover:text-emerald-300 underline">
            Sign In Here
          </Link>
        </div>
      </div>

      <div className="mt-8 flex items-center gap-2 text-xs text-slate-500">
        <ShieldCheck className="w-4 h-4 text-emerald-500" />
        <span>Stored securely in your isolated Supabase multi-tenant database</span>
      </div>
    </div>
  );
}
