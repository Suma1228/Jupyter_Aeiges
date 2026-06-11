import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { DataTable, type Column } from "@/components/ui-ext/DataTable";
import { StatusBadge, type ComplaintStatus } from "@/components/ui-ext/StatusBadge";
import { PriorityIndicator, type Priority } from "@/components/ui-ext/PriorityIndicator";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { Filter, Download, CheckCircle } from "lucide-react";
import { useEffect, useState } from "react";
import api from "@/lib/api/client";

interface OpsComplaintRow {
  id: string;
  reference: string;
  customer: string;
  category: string;
  priority: Priority;
  status: ComplaintStatus;
  assignee: string;
  sla: string;
}

export const Route = createFileRoute("/ops/complaints")({
  head: () => ({ meta: [{ title: "Complaints Queue — Aegis Ops" }] }),
  component: OpsComplaints,
});

function OpsComplaints() {
  const [rows, setRows] = useState<OpsComplaintRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [resolving, setResolving] = useState<string | null>(null); // ← NEW

  useEffect(() => {
    loadComplaints();
  }, []);

  const loadComplaints = async () => {
    try {
      const res = await api.get("/api/ops/complaints"); // ← fixed endpoint
      const data: OpsComplaintRow[] = res.data.map((c: any) => ({
        id: c.id,
        reference: c.complaint_number,
        customer: c.policy_number ?? "-",
        category: c.category ?? "-",
        priority: (c.priority ?? "LOW") as Priority,
        status: (c.status ?? "NEW") as ComplaintStatus,
        assignee: c.assigned_team?.name ?? "-",
        sla: c.sla_due_at
          ? new Date(c.sla_due_at).toLocaleDateString()
          : "-",
      }));
      setRows(data);
    } catch (err) {
      console.error("Failed to load ops complaints", err);
    } finally {
      setLoading(false);
    }
  };

  // ← NEW: calls PUT /api/ops/complaints/{id}/resolve
  const handleResolve = async (id: string) => {
  setResolving(id);
  try {
    await api.put(`/api/ops/complaints/${id}/resolve`, {});
    setRows((prev) =>
      prev.map((r) =>
        r.id === id ? { ...r, status: "RESOLVED" as ComplaintStatus } : r
      )
    );
  } catch (err: any) {
    // ← Detailed logging
    console.error("Status:", err.response?.status);
    console.error("Detail:", err.response?.data);
    alert(`Error ${err.response?.status}: ${JSON.stringify(err.response?.data)}`);
  } finally {
    setResolving(null);
  }
};

  const columns: Column<OpsComplaintRow>[] = [
    {
      key: "reference",
      header: "Ref",
      className: "font-mono text-xs text-muted-foreground",
    },
    { key: "customer", header: "Customer" },
    { key: "category", header: "Category" },
    {
      key: "priority",
      header: "Priority",
      render: (r) => <PriorityIndicator priority={r.priority} />,
    },
    {
      key: "status",
      header: "Status",
      render: (r) => <StatusBadge status={r.status} />,
    },
    {
      key: "assignee",
      header: "Assignee",
      className: "text-xs text-muted-foreground",
    },
    {
      key: "sla",
      header: "SLA",
      className: "font-mono text-xs",
    },
    // ← NEW: Action column
    {
      key: "id",
      header: "Action",
      render: (r) =>
        r.status === "RESOLVED" ? (
          <span className="inline-flex items-center gap-1 text-xs text-emerald-500 font-medium">
            <CheckCircle className="h-3.5 w-3.5" />
            Resolved
          </span>
        ) : (
          <button
            onClick={() => handleResolve(r.id)}
            disabled={resolving === r.id}
            className="inline-flex items-center gap-1.5 rounded-lg bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-400 transition hover:bg-emerald-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <CheckCircle className="h-3.5 w-3.5" />
            {resolving === r.id ? "Resolving…" : "Resolve"}
          </button>
        ),
    },
  ];

  return (
    <AppShell
      role="ops"
      title="Complaints Queue"
      subtitle="Filter, triage, and assign across the entire complaint pipeline."
      actions={
        <button className="glass hidden items-center gap-2 rounded-xl px-3 py-2 text-xs font-medium text-foreground transition hover:bg-accent/40 sm:inline-flex">
          <Download className="h-3.5 w-3.5" />
          Export
        </button>
      }
    >
      <GlassPanel className="mb-4 p-3">
        <div className="flex flex-wrap items-center gap-2">
          <span className="inline-flex items-center gap-1.5 rounded-lg bg-muted px-2.5 py-1.5 font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
            <Filter className="h-3 w-3" />
            Filters
          </span>
          {["All statuses", "All priorities", "All categories", "All assignees"].map((f) => (
            <button
              key={f}
              className="rounded-lg border border-border bg-background/40 px-3 py-1.5 text-xs text-foreground transition hover:bg-accent/30"
            >
              {f}
            </button>
          ))}
        </div>
      </GlassPanel>

      <DataTable<OpsComplaintRow>
        columns={columns}
        rows={rows}
        loading={loading}
        emptyTitle="No complaints in queue"
        emptyDescription="When complaints are submitted, they'll stream into this table for triage and assignment."
      />
    </AppShell>
  );
}