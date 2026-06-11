import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { EmptyState } from "@/components/ui-ext/EmptyState";
import { Search, Radar } from "lucide-react";
import { useState } from "react";
import api from "@/lib/api/client";
import { StatusBadge, type ComplaintStatus } from "@/components/ui-ext/StatusBadge";
import { PriorityIndicator, type Priority } from "@/components/ui-ext/PriorityIndicator";

export const Route = createFileRoute("/customer/track")({
  head: () => ({ meta: [{ title: "Track Complaint — Aegis" }] }),
  component: TrackComplaint,
});

function TrackComplaint() {
  const [complaintId, setComplaintId] = useState("");
  const [complaint, setComplaint] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleTrack = async () => {
    if (!complaintId.trim()) return;

    try {
      setLoading(true);
      setError("");
      setComplaint(null);

      const res = await api.get(
        `/api/complaints/${complaintId.trim()}`
      );

      console.log("Complaint:", res.data);

      setComplaint(res.data);
    } catch (err: any) {
      console.error(err);

      setError(
        err?.response?.data?.detail ||
          "Complaint not found"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppShell
      role="customer"
      title="Track Complaint"
      subtitle="Enter a reference number to see live status, timeline, and AI insights."
    >
      <GlassPanel className="p-6">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleTrack();
          }}
          className="flex flex-col gap-3 sm:flex-row sm:items-center"
        >
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />

            <input
              type="text"
              value={complaintId}
              onChange={(e) =>
                setComplaintId(e.target.value)
              }
              placeholder="Enter Complaint UUID"
              className="w-full rounded-xl border border-border bg-input/40 py-3 pl-10 pr-3 font-mono text-sm text-foreground placeholder:text-muted-foreground focus:border-primary/60 focus:outline-none focus:ring-2 focus:ring-primary/30"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-sm font-medium text-primary-foreground transition hover:opacity-90 glow-ring"
          >
            <Radar className="h-4 w-4" />
            {loading ? "Tracking..." : "Track"}
          </button>
        </form>
      </GlassPanel>

      {error && (
        <div className="mt-6">
          <GlassPanel className="p-4">
            <p className="text-sm text-destructive">
              {error}
            </p>
          </GlassPanel>
        </div>
      )}

      {complaint && (
        <div className="mt-6">
          <GlassPanel className="p-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">
                Complaint Details
              </h3>

              <div>
                <span className="font-medium">ID:</span>
                <div className="font-mono text-sm mt-1">
                  {complaint.id}
                </div>
              </div>

              <div>
                <span className="font-medium">Title:</span>
                <div className="mt-1">
                  {complaint.title}
                </div>
              </div>

              <div>
                <span className="font-medium">
                  Description:
                </span>
                <div className="mt-1 text-muted-foreground">
                  {complaint.description}
                </div>
              </div>

              <div className="flex flex-wrap gap-6">
                <div>
                  <div className="mb-2 text-sm font-medium">
                    Priority
                  </div>

                  <PriorityIndicator
                    priority={
                      String(
                        complaint.priority ?? "medium"
                      ).toLowerCase() as Priority
                    }
                  />
                </div>

                <div>
                  <div className="mb-2 text-sm font-medium">
                    Status
                  </div>

                  <StatusBadge
                    status={
                      String(
                        complaint.status ?? "new"
                      ).toLowerCase() as ComplaintStatus
                    }
                  />
                </div>
              </div>

              <div>
                <span className="font-medium">
                  Created At:
                </span>
                <div className="mt-1 text-sm text-muted-foreground">
                  {complaint.created_at
                    ? new Date(
                        complaint.created_at
                      ).toLocaleString()
                    : "-"}
                </div>
              </div>

              <div>
                <span className="font-medium">
                  Updated At:
                </span>
                <div className="mt-1 text-sm text-muted-foreground">
                  {complaint.updated_at
                    ? new Date(
                        complaint.updated_at
                      ).toLocaleString()
                    : "-"}
                </div>
              </div>
            </div>
          </GlassPanel>
        </div>
      )}

      {!complaint && !error && (
        <div className="mt-6">
          <GlassPanel>
            <EmptyState
              icon={Radar}
              title="Awaiting tracking input"
              description="Once you enter a complaint ID, we'll display its latest status and details."
            />
          </GlassPanel>
        </div>
      )}
    </AppShell>
  );
}
