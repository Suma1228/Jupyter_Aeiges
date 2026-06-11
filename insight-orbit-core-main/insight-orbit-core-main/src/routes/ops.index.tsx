import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { KpiCard } from "@/components/ui-ext/KpiCard";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { ChartPlaceholder } from "@/components/ui-ext/ChartPlaceholder";
import { EmptyState } from "@/components/ui-ext/EmptyState";
import {
  Inbox,
  Layers,
  Flame,
  Timer,
  CheckCircle2,
  Sparkles,
} from "lucide-react";
import { useEffect, useState } from "react";

export const Route = createFileRoute("/ops/")({
  head: () => ({ meta: [{ title: "Operations Dashboard — Aegis" }] }),
  component: OpsDashboard,
});

function OpsDashboard() {
  const [authorized, setAuthorized] = useState<boolean | null>(null);

  useEffect(() => {
    const role = localStorage.getItem("user_role");

    if (role === "OPS") {
      setAuthorized(true);
    } else {
      setAuthorized(false);
    }
  }, []);

  // ⛔ loading state (prevents flicker)
  if (authorized === null) {
    return (
      <div className="p-6 text-muted-foreground">
        Checking access...
      </div>
    );
  }

  // ⛔ unauthorized access
  if (!authorized) {
    return (
      <div className="p-6 text-red-500 font-semibold">
        Unauthorized — Ops only access
      </div>
    );
  }

  return (
    <AppShell
      role="ops"
      title="Operations Dashboard"
      subtitle="Real-time situational awareness across the complaint queue."
    >
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <KpiCard
          label="Total Complaints"
          value="—"
          icon={Layers}
          accent="primary"
          hint="Open queue"
        />
        <KpiCard
          label="High Priority"
          value="—"
          icon={Flame}
          accent="destructive"
          hint="P1 / P2"
        />
        <KpiCard
          label="SLA Risk"
          value="—"
          icon={Timer}
          accent="warning"
          hint="< 4h to breach"
        />
        <KpiCard
          label="Resolved Today"
          value="—"
          icon={CheckCircle2}
          accent="success"
          hint="Last 24h"
        />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <GlassPanel className="p-5 lg:col-span-2">
          <ChartPlaceholder
            title="Inflow vs. resolution"
            subtitle="Rolling 14-day complaint throughput"
            height={300}
          />
        </GlassPanel>

        <GlassPanel className="p-5">
          <ChartPlaceholder
            title="Category mix"
            subtitle="Share of open complaints by type"
            height={300}
          />
        </GlassPanel>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <GlassPanel className="p-5 lg:col-span-2">
          <div className="mb-4 flex items-center justify-between">
            <div>
              <h2 className="font-display text-base font-semibold text-foreground">
                Live queue
              </h2>
              <p className="text-xs text-muted-foreground">
                Highest-priority unassigned complaints in real time.
              </p>
            </div>

            <span className="inline-flex items-center gap-1.5 rounded-full bg-success/10 px-2.5 py-1 text-[11px] font-medium text-success ring-1 ring-success/30">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-success" />
              Live
            </span>
          </div>

          <EmptyState
            icon={Inbox}
            title="Queue is empty"
            description="When new complaints arrive, they will stream into this panel and be triaged automatically."
          />
        </GlassPanel>

        <GlassPanel className="p-5">
          <div className="mb-4 flex items-center gap-2">
            <Sparkles className="h-4 w-4 text-primary" />
            <h2 className="font-display text-base font-semibold text-foreground">
              AI signals
            </h2>
          </div>

          <ul className="space-y-3">
            {[
              "Pattern detection idle — no anomalies in the last interval.",
              "Sentiment monitor ready.",
              "Predictive SLA model loaded.",
            ].map((t) => (
              <li
                key={t}
                className="flex items-start gap-2 rounded-xl border border-border/60 bg-background/30 p-3 text-xs text-muted-foreground"
              >
                <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-primary" />
                {t}
              </li>
            ))}
          </ul>
        </GlassPanel>
      </div>
    </AppShell>
  );
}