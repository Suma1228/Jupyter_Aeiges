import { createFileRoute } from "@tanstack/react-router";
import { AppShell } from "@/components/layout/AppShell";
import { GlassPanel } from "@/components/ui-ext/GlassPanel";
import { EmptyState } from "@/components/ui-ext/EmptyState";
import { Sparkles } from "lucide-react";

export const Route = createFileRoute("/customer/insights")({
  head: () => ({ meta: [{ title: "AI Insights — Aegis" }] }),
  component: () => (
    <AppShell
      role="customer"
      title="AI Insights"
      subtitle="Personalized recommendations and explanations from your AI assistant."
    >
      <GlassPanel>
        <EmptyState
          icon={Sparkles}
          title="Insights will appear here"
          description="Once you have active complaints, your AI assistant will surface explanations, next steps, and outcome predictions."
        />
      </GlassPanel>
    </AppShell>
  ),
});
