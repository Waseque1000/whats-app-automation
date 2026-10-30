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
  MessageSquare,
  LogOut
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
    <aside className="w-64 bg-white border-r border-slate-200 flex flex-col justify-between h-screen sticky top-0 shadow-sm">
      {/* Brand Header */}
      <div>
        <div className="h-16 px-6 flex items-center justify-between border-b border-slate-200">
          <Link href="/" className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-emerald-600 flex items-center justify-center text-white font-bold shadow-sm">
              <MessageSquare className="w-4 h-4 fill-white text-white" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-sm tracking-tight text-slate-900">WhatsPulse</span>
              <span className="text-[10px] text-emerald-700 font-bold">SaaS Cloud</span>
            </div>
          </Link>
          <span className="text-[10px] uppercase font-extrabold px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
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
                    ? "bg-emerald-50 text-emerald-800 font-bold border border-emerald-200/80 shadow-xs"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-50"
                }`}
              >
                <div className="flex items-center gap-3">
                  <Icon className={`w-4 h-4 ${isActive ? "text-emerald-700 font-bold" : "text-slate-400"}`} />
                  <span>{item.label}</span>
                </div>

                {item.badge && !isActive && (
                  <span className="text-[9px] uppercase font-extrabold px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700 border border-emerald-200">
                    {item.badge}
                  </span>
                )}
                {item.pulse && !isActive && (
                  <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* User & Session Footer */}
      <div className="p-4 border-t border-slate-200 space-y-3 bg-slate-50/50">
        {/* Device Status Card */}
        <Link
          href="/app/connect"
          className="block p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-400 hover:shadow-xs transition-all text-xs"
        >
          <div className="flex items-center justify-between mb-1">
            <span className="text-[11px] font-bold text-slate-700">WhatsApp Device</span>
            <span className="flex items-center gap-1 text-[10px] font-bold text-emerald-700">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Online
            </span>
          </div>
          <div className="text-[11px] font-mono text-slate-500 font-medium">
            +880 1800-123456
          </div>
        </Link>

        {/* User Profile */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-full bg-emerald-100 border border-emerald-200 flex items-center justify-center font-bold text-xs text-emerald-800">
              WA
            </div>
            <div className="flex flex-col text-left">
              <span className="text-xs font-bold text-slate-800">Waseque Admin</span>
              <span className="text-[10px] text-slate-500">Durber Academy</span>
            </div>
          </div>
          <Link href="/" className="text-slate-400 hover:text-slate-600 transition-colors" title="Back to Website">
            <LogOut className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </aside>
  );
}
