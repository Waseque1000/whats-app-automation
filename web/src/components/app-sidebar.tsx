"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  Send,
  Users,
  FileText,
  QrCode,
  BarChart3,
  Settings,
  Shield,
  MessageSquare,
  LogOut,
  ChevronRight
} from "lucide-react";

export function AppSidebar() {
  const pathname = usePathname();

  const navItems = [
    { label: "Overview", href: "/app", icon: LayoutDashboard },
    { label: "Campaigns", href: "/app/campaigns", icon: Send, badge: "Anti-Ban" },
    { label: "Message Variants", href: "/app/templates", icon: FileText },
    { label: "Contacts & Students", href: "/app/students", icon: Users },
    { label: "WhatsApp Connect", href: "/app/connect", icon: QrCode, pulse: true },
    { label: "Reports & Audit", href: "/app/reports", icon: BarChart3 },
    { label: "Settings & Billing", href: "/app/settings", icon: Settings },
  ];

  return (
    <aside className="w-64 bg-slate-950 border-r border-slate-850 flex flex-col justify-between h-screen sticky top-0">
      {/* Brand Header */}
      <div>
        <div className="h-16 px-6 flex items-center justify-between border-b border-slate-850">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-emerald-500 flex items-center justify-center text-slate-950 font-bold">
              <MessageSquare className="w-4 h-4 fill-slate-950" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-sm tracking-tight text-white">WhatsPulse</span>
              <span className="text-[10px] text-emerald-400 font-medium">SaaS Cloud</span>
            </div>
          </Link>
          <span className="text-[10px] uppercase font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            PRO
          </span>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3.5 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                  isActive
                    ? "bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/15"
                    : "text-slate-400 hover:text-white hover:bg-slate-900"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? "text-slate-950" : "text-slate-400"}`} />
                  <span>{item.label}</span>
                </div>

                {item.badge && !isActive && (
                  <span className="text-[9px] uppercase font-extrabold px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    {item.badge}
                  </span>
                )}
                {item.pulse && !isActive && (
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* User & Session Footer */}
      <div className="p-4 border-t border-slate-850 space-y-3">
        {/* Device Status Card */}
        <Link
          href="/app/connect"
          className="block p-3 rounded-xl bg-slate-900/80 border border-slate-800 hover:border-emerald-500/30 transition-all text-xs"
        >
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-semibold text-slate-300">WhatsApp Device</span>
            <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Online
            </span>
          </div>
          <div className="text-[11px] font-mono text-slate-400">
            +880 1800-123456
          </div>
        </Link>

        {/* User Profile */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs text-emerald-400">
              WA
            </div>
            <div className="flex flex-col text-left">
              <span className="text-xs font-semibold text-white">Waseque Admin</span>
              <span className="text-[10px] text-slate-500">Durber Academy</span>
            </div>
          </div>
          <Link href="/" className="text-slate-500 hover:text-slate-300 transition-colors" title="Back to Website">
            <LogOut className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </aside>
  );
}

