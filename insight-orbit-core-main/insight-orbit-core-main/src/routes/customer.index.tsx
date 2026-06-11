import { createFileRoute, Link, useNavigate } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { KpiCard } from "@/components/ui-ext/KpiCard";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { EmptyState } from "@/components/ui-ext/EmptyState";
import { ChartPlaceholder } from "@/components/ui-ext/ChartPlaceholder";
import {
  FileText,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Plus,
  Inbox,
} from "lucide-react";

export const Route = createFileRoute("/customer/")({
  head: () => ({
    meta: [{ title: "My Dashboard — Aegis" }],
  }),
  component: CustomerDashboard,
});

function CustomerDashboard() {
  const navigate = useNavigate();

  return (
    <AppShell
      role="customer"
      title="My Dashboard"
      subtitle="Track and manage your insurance complaints."
      actions={
        <Link
          to="/customer/raise"
          className="hidden items-center gap-2 rounded-xl bg-primary px-3.5 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90 glow-ring sm:inline-flex"
        >
          <Plus className="h-4 w-4" />
          Raise Complaint
        </Link>
      }
    >
      {/* KPI CARDS */}
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <div
          className="cursor-pointer transition hover:scale-[1.02]"
          onClick={() => navigate({ to: "/customer/complaints" })}
        >
          <KpiCard
            label="My Complaints"
            value="—"
            icon={FileText}
            accent="primary"
            hint="All time"
          />
        </div>

        <div
          className="cursor-pointer transition hover:scale-[1.02]"
          onClick={() =>
            navigate({
              to: "/customer/complaints",
              search: { status: "IN_PROGRESS" } as never,
            })
          }
        >
          <KpiCard
            label="In Progress"
            value="—"
            icon={Clock}
            accent="info"
            hint="Active cases"
          />
        </div>

        <div
          className="cursor-pointer transition hover:scale-[1.02]"
          onClick={() =>
            navigate({
              to: "/customer/complaints",
              search: { status: "AWAITING_CUSTOMER" } as never,
            })
          }
        >
          <KpiCard
            label="Awaiting You"
            value="—"
            icon={AlertTriangle}
            accent="warning"
            hint="Action required"
          />
        </div>

        <div
          className="cursor-pointer transition hover:scale-[1.02]"
          onClick={() =>
            navigate({
              to: "/customer/complaints",
              search: { status: "RESOLVED" } as never,
            })
          }
        >
          <KpiCard
            label="Resolved"
            value="—"
            icon={CheckCircle2}
            accent="success"
            hint="Last 90 days"
          />
        </div>
      </div>

      {/* CHARTS */}
      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <GlassPanel className="p-5 lg:col-span-2">
          <ChartPlaceholder
            title="Complaint activity"
            subtitle="Status changes over the last 30 days"
            height={300}
          />
        </GlassPanel>

        <GlassPanel className="p-5">
          <ChartPlaceholder
            title="Resolution time"
            subtitle="Median days to resolve"
            height={300}
          />
        </GlassPanel>
      </div>

      {/* RECENT COMPLAINTS */}
      <div className="mt-6">
        <div className="mb-3 flex items-end justify-between">
          <div>
            <h2 className="font-display text-lg font-semibold text-foreground">
              Recent complaints
            </h2>
            <p className="text-xs text-muted-foreground">
              Your most recent submissions and their live status.
            </p>
          </div>

          <Link
            to="/customer/complaints"
            className="text-xs font-medium text-primary hover:underline"
          >
            View all →
          </Link>
        </div>

        <GlassPanel>
          <EmptyState
            icon={Inbox}
            title="No complaints yet"
            description="When you raise a complaint, it will appear here with a live status timeline."
            action={
              <Link
                to="/customer/raise"
                className="inline-flex items-center gap-2 rounded-xl bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition hover:opacity-90"
              >
                <Plus className="h-4 w-4" />
                Raise your first complaint
              </Link>
            }
          />
        </GlassPanel>
      </div>
    </AppShell>
  );
}

export default CustomerDashboard;