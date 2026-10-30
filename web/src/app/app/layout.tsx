import { AppSidebar } from "../../components/app-sidebar";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-[#090d16] text-slate-100 flex">
      {/* SaaS Sidebar */}
      <AppSidebar />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Top bar */}
        <header className="h-16 px-8 border-b border-slate-850 flex items-center justify-between bg-slate-950/60 sticky top-0 z-30 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold text-slate-400">Workspace:</span>
            <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs font-semibold text-white">
              Durber Coaching &bull; Main Branch
            </span>
          </div>

          <div className="flex items-center gap-4 text-xs">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Anti-Restriction Active (v2.4)</span>
            </div>

            <span className="text-slate-500">|</span>

            <div className="flex items-center gap-2">
              <span className="text-slate-400">Monthly Quota:</span>
              <strong className="text-white font-mono">1,420 / 25,000 msgs</strong>
            </div>
          </div>
        </header>

        {/* Page children */}
        <div className="p-8 max-w-7xl w-full mx-auto space-y-8">
          {children}
        </div>
      </main>
    </div>
  );
}

