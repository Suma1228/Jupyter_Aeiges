import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { ChartPlaceholder } from "@/components/ui-ext/ChartPlaceholder";
import { KpiCard } from "@/components/ui-ext/KpiCard";
import { Activity, Gauge, Clock4, ThumbsUp } from "lucide-react";

export const Route = createFileRoute("/ops/analytics")({
  head: () => ({ meta: [{ title: "Analytics — Aegis Ops" }] }),
  component: OpsAnalytics,
});

function OpsAnalytics() {
  return (
    <AppShell
      role="ops"
      title="Analytics"
      subtitle="Operational performance across teams, channels, and policy lines."
    >
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <KpiCard label="Volume (7d)" value="—" icon={Activity} accent="primary" />
        <KpiCard label="SLA attainment" value="—" icon={Gauge} accent="success" />
        <KpiCard label="Avg. resolution" value="—" icon={Clock4} accent="info" />
        <KpiCard label="CSAT" value="—" icon={ThumbsUp} accent="warning" />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        <GlassPanel className="p-5">
          <ChartPlaceholder title="Volume by channel" subtitle="Web · Mobile · Phone · Email" height={280} />
        </GlassPanel>
        <GlassPanel className="p-5">
          <ChartPlaceholder title="Resolution time distribution" subtitle="Hours to close" height={280} />
        </GlassPanel>
        <GlassPanel className="p-5">
          <ChartPlaceholder title="Agent leaderboard" subtitle="Throughput and quality" height={280} />
        </GlassPanel>
        <GlassPanel className="p-5">
          <ChartPlaceholder title="Root cause heatmap" subtitle="Category × policy line" height={280} />
        </GlassPanel>
      </div>
    </AppShell>
  );
}
