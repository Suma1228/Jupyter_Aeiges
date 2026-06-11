import { type LucideIcon, ArrowDownRight, ArrowUpRight, Minus } from "lucide-react";
import { GlassPanel } from "./GlassPanel";
import { cn } from "@/lib/utils";

export interface KpiCardProps {
  label: string;
  value: string | number;
  icon?: LucideIcon;
  /** Percentage change vs previous period. Omit when no data is available. */
  delta?: number;
  hint?: string;
  accent?: "primary" | "success" | "warning" | "destructive" | "info";
}

const accentRing: Record<NonNullable<KpiCardProps["accent"]>, string> = {
  primary: "from-primary/30 to-primary/0",
  success: "from-success/30 to-success/0",
  warning: "from-warning/30 to-warning/0",
  destructive: "from-destructive/30 to-destructive/0",
  info: "from-info/30 to-info/0",
};

const accentIcon: Record<NonNullable<KpiCardProps["accent"]>, string> = {
  primary: "text-primary bg-primary/10 ring-primary/30",
  success: "text-success bg-success/10 ring-success/30",
  warning: "text-warning bg-warning/10 ring-warning/30",
  destructive: "text-destructive bg-destructive/10 ring-destructive/30",
  info: "text-info bg-info/10 ring-info/30",
};

export function KpiCard({
  label,
  value,
  icon: Icon,
  delta,
  hint,
  accent = "primary",
}: KpiCardProps) {
  const trendIcon =
    delta === undefined ? Minus : delta > 0 ? ArrowUpRight : delta < 0 ? ArrowDownRight : Minus;
  const TrendIcon = trendIcon;
  const trendClass =
    delta === undefined
      ? "text-muted-foreground"
      : delta > 0
        ? "text-success"
        : delta < 0
          ? "text-destructive"
          : "text-muted-foreground";

  return (
    <GlassPanel className="relative overflow-hidden p-5">
      <div
        className={cn(
          "pointer-events-none absolute -right-10 -top-10 h-32 w-32 rounded-full bg-gradient-radial blur-2xl",
          `bg-gradient-to-br ${accentRing[accent]}`,
        )}
      />
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-1">
          <p className="font-mono text-[11px] uppercase tracking-[0.18em] text-muted-foreground">
            {label}
          </p>
          <p className="text-3xl font-semibold tracking-tight text-foreground">{value}</p>
        </div>
        {Icon && (
          <div className={cn("rounded-xl p-2.5 ring-1", accentIcon[accent])}>
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>
      <div className="mt-4 flex items-center justify-between text-xs">
        <span className={cn("inline-flex items-center gap-1 font-medium", trendClass)}>
          <TrendIcon className="h-3.5 w-3.5" />
          {delta === undefined ? "No baseline" : `${delta > 0 ? "+" : ""}${delta}%`}
        </span>
        {hint && <span className="text-muted-foreground">{hint}</span>}
      </div>
    </GlassPanel>
  );
}
