import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { Sparkles, Brain, Radar, ShieldAlert } from "lucide-react";
import { type LucideIcon } from "lucide-react";

export const Route = createFileRoute("/ops/insights")({
  head: () => ({ meta: [{ title: "AI Insights — Aegis Ops" }] }),
  component: OpsInsights,
});

interface AgentCardProps {
  icon: LucideIcon;
  name: string;
  description: string;
  status: "ready" | "training" | "offline";
}

function AgentCard({ icon: Icon, name, description, status }: AgentCardProps) {
  const statusCfg = {
    ready: { label: "Ready", cls: "bg-success/10 text-success ring-success/30", dot: "bg-success" },
    training: { label: "Training", cls: "bg-warning/10 text-warning ring-warning/30", dot: "bg-warning" },
    offline: { label: "Offline", cls: "bg-muted text-muted-foreground ring-border", dot: "bg-muted-foreground" },
  }[status];

  return (
    <GlassPanel className="group relative overflow-hidden p-5 transition hover:ring-1 hover:ring-primary/30">
      <div className="pointer-events-none absolute -right-12 -top-12 h-32 w-32 rounded-full bg-primary/15 blur-2xl transition group-hover:bg-primary/25" />
      <div className="flex items-start justify-between gap-3">
        <div className="grid h-10 w-10 place-items-center rounded-xl bg-primary/10 ring-1 ring-primary/30">
          <Icon className="h-5 w-5 text-primary" />
        </div>
        <span
          className={`inline-flex items-center gap-1.5 rounded-full px-2 py-1 text-[11px] font-medium ring-1 ${statusCfg.cls}`}
        >
          <span className={`h-1.5 w-1.5 rounded-full ${statusCfg.dot}`} />
          {statusCfg.label}
        </span>
      </div>
      <h3 className="mt-4 font-display text-base font-semibold text-foreground">{name}</h3>
      <p className="mt-1 text-sm leading-relaxed text-muted-foreground">{description}</p>
    </GlassPanel>
  );
}

function OpsInsights() {
  return (
    <AppShell
      role="ops"
      title="AI Insights"
      subtitle="The intelligence layer powering triage, routing, and resolution."
    >
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <AgentCard
          icon={Brain}
          name="Triage Agent"
          description="Classifies complaints, scores severity, and proposes routing within seconds."
          status="ready"
        />
        <AgentCard
          icon={Radar}
          name="Pattern Detector"
          description="Surfaces emerging issues, clusters, and systemic risks across the queue."
          status="ready"
        />
        <AgentCard
          icon={ShieldAlert}
          name="SLA Sentinel"
          description="Predicts SLA breaches and recommends interventions before deadlines slip."
          status="training"
        />
        <AgentCard
          icon={Sparkles}
          name="Resolution Copilot"
          description="Drafts responses, cites policy clauses, and suggests next best actions."
          status="ready"
        />
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-3">
        <GlassPanel className="p-5 lg:col-span-2">
          <h2 className="font-display text-base font-semibold text-foreground">Recent signals</h2>
          <p className="text-xs text-muted-foreground">
            Anomalies and patterns surfaced by the intelligence layer.
          </p>
          <div className="mt-4 rounded-xl border border-dashed border-border/70 bg-background/30 p-8 text-center text-sm text-muted-foreground">
            No anomalies detected. The intelligence layer is monitoring continuously.
          </div>
        </GlassPanel>
        <GlassPanel className="p-5">
          <h2 className="font-display text-base font-semibold text-foreground">Model registry</h2>
          <ul className="mt-4 space-y-2 font-mono text-xs">
            {[
              ["triage-classifier", "v2.4.1"],
              ["severity-scorer", "v1.8.0"],
              ["sla-predictor", "v0.9.3 (rc)"],
              ["resolution-llm", "v3.0.0"],
            ].map(([name, ver]) => (
              <li
                key={name}
                className="flex items-center justify-between rounded-lg border border-border/60 bg-background/30 px-3 py-2"
              >
                <span className="text-foreground">{name}</span>
                <span className="text-muted-foreground">{ver}</span>
              </li>
            ))}
          </ul>
        </GlassPanel>
      </div>
    </AppShell>
  );
}
