"use client";

import { useState, useEffect } from "react";
import {
  QrCode,
  Smartphone,
  RefreshCw,
  CheckCircle2,
  AlertCircle,
  Shield,
  Wifi,
  BatteryCharging
} from "lucide-react";
import { INITIAL_DEVICE_SESSION } from "../../../lib/mock-data";

export default function ConnectPage() {
  const [session, setSession] = useState(INITIAL_DEVICE_SESSION);
  const [countdown, setCountdown] = useState(25);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    if (!session.connected) {
      const timer = setInterval(() => {
        setCountdown((c) => (c > 1 ? c - 1 : 30));
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [session.connected]);

  const handleToggleConnection = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setSession(prev => ({
        ...prev,
        connected: !prev.connected,
        statusText: !prev.connected ? "Ready & Active" : "Disconnected (Scan QR)"
      }));
      setIsRefreshing(false);
    }, 600);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
          <span>WhatsApp Web Cloud Session Hub</span>
          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold ${
            session.connected ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20" : "bg-amber-500/10 text-amber-400 border border-amber-500/20"
          }`}>
            {session.connected ? "● Connected" : "○ Disconnected"}
          </span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Connect your physical or business phone number directly to the SaaS cloud dispatcher using standard Linked Devices.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-start">
        {/* QR Code Card */}
        <div className="md:col-span-6 glass-panel p-6 rounded-2xl border border-slate-800 text-center space-y-4">
          <div className="flex items-center justify-between pb-3 border-b border-slate-850">
            <span className="text-xs font-semibold text-slate-300">WhatsApp Web QR Code</span>
            {!session.connected && (
              <span className="text-[11px] font-mono text-emerald-400">
                Auto-refreshes in {countdown}s
              </span>
            )}
          </div>

          <div className="p-6 bg-white rounded-2xl inline-block shadow-2xl relative">
            {session.connected ? (
              <div className="w-56 h-56 flex flex-col items-center justify-center bg-slate-900 rounded-xl text-emerald-400 space-y-2 p-4">
                <CheckCircle2 className="w-12 h-12" />
                <span className="font-bold text-xs text-white">Device Linked &amp; Active</span>
                <span className="text-[10px] text-slate-400 text-center font-mono">
                  {session.phoneNumber}
                </span>
              </div>
            ) : (
              <div className="w-56 h-56 flex flex-col items-center justify-center relative">
                {/* SVG QR Code Simulation */}
                <svg className="w-full h-full text-slate-950" viewBox="0 0 100 100" fill="currentColor">
                  {/* Top-left marker */}
                  <rect x="5" y="5" width="25" height="25" rx="3" fill="#000" />
                  <rect x="9" y="9" width="17" height="17" fill="#fff" />
                  <rect x="13" y="13" width="9" height="9" fill="#000" />
                  
                  {/* Top-right marker */}
                  <rect x="70" y="5" width="25" height="25" rx="3" fill="#000" />
                  <rect x="74" y="9" width="17" height="17" fill="#fff" />
                  <rect x="78" y="13" width="9" height="9" fill="#000" />

                  {/* Bottom-left marker */}
                  <rect x="5" y="70" width="25" height="25" rx="3" fill="#000" />
                  <rect x="9" y="74" width="17" height="17" fill="#fff" />
                  <rect x="13" y="78" width="9" height="9" fill="#000" />

                  {/* Data blocks */}
                  <rect x="35" y="10" width="8" height="8" fill="#000" />
                  <rect x="48" y="15" width="12" height="6" fill="#000" />
                  <rect x="38" y="30" width="24" height="24" fill="#000" />
                  <rect x="68" y="40" width="10" height="8" fill="#000" />
                  <rect x="10" y="42" width="12" height="12" fill="#000" />
                  <rect x="40" y="70" width="15" height="8" fill="#000" />
                  <rect x="70" y="70" width="18" height="18" fill="#000" />
                </svg>
              </div>
            )}
          </div>

          <div className="pt-2">
            <button
              onClick={handleToggleConnection}
              disabled={isRefreshing}
              className="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-200 text-xs font-semibold border border-slate-800 transition-colors flex items-center justify-center gap-2"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-emerald-400" : ""}`} />
              <span>{session.connected ? "Disconnect & Regenerate QR" : "Simulate Successful QR Scan"}</span>
            </button>
          </div>
        </div>

        {/* Instructions and Session Info */}
        <div className="md:col-span-6 space-y-6">
          <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <Smartphone className="w-4 h-4 text-emerald-400" />
              <span>How to Connect Your Phone</span>
            </h2>

            <ol className="space-y-3 text-xs text-slate-300 list-decimal list-inside leading-relaxed">
              <li>Open <strong>WhatsApp</strong> on your mobile device.</li>
              <li>Tap <strong>Settings</strong> or the three dots <strong>⋮</strong> &gt; <strong>Linked Devices</strong>.</li>
              <li>Tap <strong>Link a Device</strong> and point your camera at this QR code.</li>
              <li>Once scanned, your cloud session activates with 24/7 background availability.</li>
            </ol>
          </div>

          {session.connected && (
            <div className="glass-panel p-6 rounded-2xl border border-emerald-500/30 space-y-3 bg-emerald-950/10">
              <h3 className="text-xs font-bold text-emerald-400 uppercase tracking-wider">
                Session Diagnostics
              </h3>

              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-slate-850">
                  <span className="text-slate-400">Phone:</span>
                  <span className="font-mono font-bold text-white">{session.phoneNumber}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-850">
                  <span className="text-slate-400">Battery Level:</span>
                  <span className="font-semibold text-emerald-400 flex items-center gap-1">
                    <BatteryCharging className="w-3.5 h-3.5" /> {session.batteryLevel}% (Charging)
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-850">
                  <span className="text-slate-400">Cloud Host:</span>
                  <span className="text-slate-300">{session.browser}</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-slate-400">Status:</span>
                  <span className="text-emerald-400 font-semibold flex items-center gap-1">
                    <Wifi className="w-3.5 h-3.5" /> High Signal &bull; Ready
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
