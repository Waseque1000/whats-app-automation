"use client";

import { useState } from "react";
import {
  Users,
  Search,
  Filter,
  Plus,
  Upload,
  Download,
  CheckCircle2,
  AlertCircle,
  Trash2,
  Check
} from "lucide-react";
import { INITIAL_STUDENTS } from "../../../lib/mock-data";
import { Student } from "../../../types";

export default function StudentsPage() {
  const [students, setStudents] = useState<Student[]>(INITIAL_STUDENTS);
  const [search, setSearch] = useState("");
  const [batchFilter, setBatchFilter] = useState("All");

  // Add modal state
  const [addModalOpen, setAddModalOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [newPhone, setNewPhone] = useState("+880");
  const [newRoll, setNewRoll] = useState("");
  const [newBatch, setNewBatch] = useState("Batch-2026");

  // Import modal state
  const [importModalOpen, setImportModalOpen] = useState(false);
  const [isImporting, setIsImporting] = useState(false);

  const filtered = students.filter((s) => {
    const matchesSearch = s.name.toLowerCase().includes(search.toLowerCase()) || s.phone.includes(search) || (s.roll && s.roll.includes(search));
    const matchesBatch = batchFilter === "All" || s.batch === batchFilter;
    return matchesSearch && matchesBatch;
  });

  const handleAddStudent = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName || !newPhone) return;

    const newStudent: Student = {
      id: Date.now(),
      name: newName,
      phone: newPhone,
      roll: newRoll,
      batch: newBatch,
      whatsappStatus: "active",
      consentStatus: "granted",
    };

    setStudents([newStudent, ...students]);
    setAddModalOpen(false);
    setNewName("");
    setNewPhone("+880");
    setNewRoll("");
  };

  const handleSimulatedImport = () => {
    setIsImporting(true);
    setTimeout(() => {
      const imported: Student[] = [
        { id: Date.now() + 1, name: "Kazi Nazrul", phone: "+8801700112233", roll: "111", batch: "Ass-7 Durber", whatsappStatus: "active", consentStatus: "granted" },
        { id: Date.now() + 2, name: "Rabeya Khatun", phone: "+8801800223344", roll: "112", batch: "Ass-7 Durber", whatsappStatus: "inactive", consentStatus: "unknown", notes: "No WhatsApp" },
        { id: Date.now() + 3, name: "Zubair Ahmed", phone: "+8801900334455", roll: "113", batch: "Ass-7 Durber", whatsappStatus: "active", consentStatus: "granted" }
      ];
      setStudents([...imported, ...students]);
      setIsImporting(false);
      setImportModalOpen(false);
    }, 800);
  };

  const handleExportCsv = () => {
    const headers = "ID,Name,Phone,Roll,Batch,WhatsApp Status,Consent\n";
    const rows = students.map(s => `"${s.id}","${s.name}","${s.phone}","${s.roll || ''}","${s.batch || ''}","${s.whatsappStatus}","${s.consentStatus}"`).join("\n");
    const blob = new Blob([headers + rows], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Contacts_Export_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight flex items-center gap-2">
            <span>Contacts &amp; Student CRM</span>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
              {students.length} Total
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Manage your recipient directory. Invalid numbers are automatically tagged and skipped during dispatch.
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => setImportModalOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-300 font-semibold text-xs border border-slate-800 transition-colors"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Import Excel/CSV</span>
          </button>
          <button
            onClick={handleExportCsv}
            className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-850 text-slate-300 font-semibold text-xs border border-slate-800 transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export CSV</span>
          </button>
          <button
            onClick={() => setAddModalOpen(true)}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition-all"
          >
            <Plus className="w-4 h-4" />
            <span>Add Contact</span>
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="glass-panel p-4 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by name, phone, or roll..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-3.5 py-2 text-xs text-white focus:outline-none focus:border-emerald-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-3.5 h-3.5 text-slate-500" />
          <span className="text-xs text-slate-400">Batch:</span>
          <select
            value={batchFilter}
            onChange={(e) => setBatchFilter(e.target.value)}
            className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-emerald-500"
          >
            <option value="All">All Batches</option>
            <option value="Ass-7 Durber">Ass-7 Durber</option>
            <option value="Batch-2026">Batch-2026</option>
          </select>
        </div>
      </div>

      {/* Students Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 font-semibold bg-slate-950/40">
                <th className="py-3 px-4">Name</th>
                <th className="py-3 px-4">Phone Number</th>
                <th className="py-3 px-4">Roll / ID</th>
                <th className="py-3 px-4">Batch</th>
                <th className="py-3 px-4">WhatsApp Status</th>
                <th className="py-3 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-850">
              {filtered.map((st) => (
                <tr key={st.id} className="hover:bg-slate-900/40 transition-colors">
                  <td className="py-3.5 px-4 font-semibold text-white">{st.name}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-300">{st.phone}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-400">{st.roll || "—"}</td>
                  <td className="py-3.5 px-4">
                    <span className="px-2 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-800 text-[11px]">
                      {st.batch}
                    </span>
                  </td>
                  <td className="py-3.5 px-4">
                    {st.whatsappStatus === "active" ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold text-[10px] border border-emerald-500/20">
                        <CheckCircle2 className="w-3 h-3" /> Active Account
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-400 font-semibold text-[10px] border border-amber-500/20" title={st.notes}>
                        <AlertCircle className="w-3 h-3" /> No WhatsApp (Auto-Skipped)
                      </span>
                    )}
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <button
                      onClick={() => setStudents(students.filter(s => s.id !== st.id))}
                      className="p-1 text-slate-500 hover:text-red-400 transition-colors"
                      title="Delete contact"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add Contact Modal */}
      {addModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel w-full max-w-md rounded-2xl p-6 border border-slate-800 shadow-2xl space-y-4">
            <h3 className="font-bold text-base text-white">Add New Contact</h3>
            <form onSubmit={handleAddStudent} className="space-y-3 text-xs">
              <div>
                <label className="text-slate-400 block mb-1">Student Full Name</label>
                <input
                  type="text"
                  required
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                  placeholder="e.g. Asif Mahmud"
                />
              </div>

              <div>
                <label className="text-slate-400 block mb-1">WhatsApp Phone Number</label>
                <input
                  type="text"
                  required
                  value={newPhone}
                  onChange={(e) => setNewPhone(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500 font-mono"
                  placeholder="+88017XXXXXXXX"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-400 block mb-1">Roll / Student ID</label>
                  <input
                    type="text"
                    value={newRoll}
                    onChange={(e) => setNewRoll(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500 font-mono"
                    placeholder="115"
                  />
                </div>
                <div>
                  <label className="text-slate-400 block mb-1">Batch / Group</label>
                  <input
                    type="text"
                    value={newBatch}
                    onChange={(e) => setNewBatch(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                    placeholder="Batch-2026"
                  />
                </div>
              </div>

              <div className="pt-3 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setAddModalOpen(false)}
                  className="px-4 py-2 rounded-xl bg-slate-900 text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-emerald-500 text-slate-950 font-bold"
                >
                  Save Contact
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Import Modal */}
      {importModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel w-full max-w-md rounded-2xl p-6 border border-slate-800 shadow-2xl space-y-4">
            <h3 className="font-bold text-base text-white flex items-center gap-2">
              <Upload className="w-4 h-4 text-emerald-400" />
              <span>Import Students via Excel / CSV</span>
            </h3>

            <div className="p-6 border-2 border-dashed border-slate-800 rounded-xl text-center space-y-2 bg-slate-950/50">
              <Upload className="w-8 h-8 text-emerald-400 mx-auto opacity-80" />
              <p className="text-xs text-slate-300 font-medium">Drag &amp; drop your .xlsx or .csv roster here</p>
              <p className="text-[11px] text-slate-500">Auto-cleans phone codes (+880), preserves leading zeros</p>
            </div>

            <div className="pt-2 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setImportModalOpen(false)}
                className="px-4 py-2 rounded-xl bg-slate-900 text-slate-400 hover:text-white text-xs font-semibold"
              >
                Cancel
              </button>
              <button
                onClick={handleSimulatedImport}
                disabled={isImporting}
                className="px-4 py-2 rounded-xl bg-emerald-500 text-slate-950 font-bold text-xs"
              >
                {isImporting ? "Processing Roster..." : "Upload & Parse"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

