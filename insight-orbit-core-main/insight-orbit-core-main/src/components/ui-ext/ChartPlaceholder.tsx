import { Activity } from "lucide-react";

interface ChartPlaceholderProps {
  title: string;
  subtitle?: string;
  height?: number;
}

/**
 * Renders an empty chart container with a futuristic grid background.
 * Used until a real data source is connected — we never display synthetic data.
 */
export function ChartPlaceholder({ title, subtitle, height = 280 }: ChartPlaceholderProps) {
  return (
    <div className="flex flex-col">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-sm font-semibold text-foreground">{title}</h3>
          {subtitle && <p className="mt-0.5 text-xs text-muted-foreground">{subtitle}</p>}
        </div>
        <span className="inline-flex items-center gap-1.5 rounded-full bg-muted px-2 py-1 font-mono text-[10px] uppercase tracking-wider text-muted-foreground ring-1 ring-border">
          <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-warning" />
          Awaiting data
        </span>
      </div>
      <div
        className="relative mt-4 grid-bg overflow-hidden rounded-xl border border-border/60 bg-background/30"
        style={{ height }}
      >
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-2 text-center">
          <Activity className="h-6 w-6 text-muted-foreground" />
          <p className="text-xs text-muted-foreground">
            Telemetry stream not yet connected
          </p>
        </div>
      </div>
    </div>
  );
}
