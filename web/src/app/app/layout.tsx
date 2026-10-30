import { AppSidebar } from "../../components/app-sidebar";

export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex">
      {/* SaaS Sidebar */}
      <AppSidebar />

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {/* Top bar */}
        <header className="h-16 px-8 border-b border-slate-200 flex items-center justify-between bg-white/90 sticky top-0 z-30 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold text-slate-500">Workspace:</span>
            <span className="px-2.5 py-1 rounded-lg bg-slate-100 border border-slate-200 text-xs font-bold text-slate-800">
              Durber Coaching &bull; Main Branch
            </span>
          </div>

          <div className="flex items-center gap-4 text-xs">
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-50 border border-emerald-200 text-emerald-800 font-bold">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>Anti-Restriction Active (v2.4)</span>
            </div>

            <span className="text-slate-300">|</span>

            <div className="flex items-center gap-2">
              <span className="text-slate-500 font-medium">Monthly Quota:</span>
              <strong className="text-slate-900 font-mono font-bold">1,420 / 25,000 msgs</strong>
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
