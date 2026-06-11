import { createFileRoute, Link } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { DataTable, type Column } from "@/components/ui-ext/DataTable";
import { StatusBadge, type ComplaintStatus } from "@/components/ui-ext/StatusBadge";
import { PriorityIndicator, type Priority } from "@/components/ui-ext/PriorityIndicator";
import { Plus } from "lucide-react";
import { useEffect, useState } from "react";
import api from "@/lib/api/client";

interface ComplaintRow {
  id: string;
  reference: string;
  subject: string;
  policy: string;
  priority: Priority;
  status: ComplaintStatus;
  updated: string;
}

export const Route = createFileRoute("/customer/complaints")({
  head: () => ({ meta: [{ title: "My Complaints — Aegis" }] }),
  component: MyComplaints,
});

function MyComplaints() {
  const [rows, setRows] = useState<ComplaintRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadComplaints();
  }, []);

  const loadComplaints = async () => {
  try {
    const res = await api.get("/api/complaints/my");

    console.log("Complaints API Response:", res.data);

    const complaints: ComplaintRow[] = res.data.map((c: any) => ({
      id: c.id,
      reference: c.id,
      subject: c.title ?? c.subject ?? "Untitled Complaint",
      policy: c.policy_number ?? "-",

      // Normalize priority
      priority: (
      String(c.priority ?? "medium").toLowerCase()
      ) as Priority,

      // Normalize status
      status: (
      String(c.status ?? "new").toLowerCase()
      ) as ComplaintStatus,

      updated: new Date(
        c.updated_at ?? c.created_at ?? Date.now()
      ).toLocaleDateString(),
    }));

    console.log("Mapped Complaints:", complaints);

    setRows(complaints);
  } catch (err) {
    console.error("Failed to load complaints", err);
  } finally {
    setLoading(false);
  }
};

  const columns: Column<ComplaintRow>[] = [
    {
      key: "reference",
      header: "Reference",
      className: "font-mono text-xs text-muted-foreground",
    },
    {
      key: "subject",
      header: "Subject",
    },
    {
      key: "policy",
      header: "Policy",
      className: "font-mono text-xs",
    },
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
      key: "updated",
      header: "Updated",
      className: "text-muted-foreground text-xs",
    },
  ];

  return (
    <AppShell
      role="customer"
      title="My Complaints"
      subtitle="All complaints you've submitted."
    >
      <DataTable<ComplaintRow>
        columns={columns}
        rows={rows}
        loading={loading}
        emptyTitle="No complaints filed"
        emptyDescription="You haven't raised any complaints yet. When you do, they'll show up here."
        emptyAction={
          <Link
            to="/customer/raise"
            className="inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90"
          >
            <Plus className="h-4 w-4" />
            Raise Complaint
          </Link>
        }
      />
    </AppShell>
  );
}