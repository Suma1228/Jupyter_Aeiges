import { cn } from "@/lib/utils";

export type Priority = "low" | "medium" | "high" | "critical";

const PRIORITY_MAP: Record<
  Priority,
  { label: string; bar: string; text: string; bars: number }
> = {
  low: {
    label: "Low",
    bar: "bg-success",
    text: "text-success",
    bars: 1,
  },
  medium: {
    label: "Medium",
    bar: "bg-info",
    text: "text-info",
    bars: 2,
  },
  high: {
    label: "High",
    bar: "bg-warning",
    text: "text-warning",
    bars: 3,
  },
  critical: {
    label: "Critical",
    bar: "bg-destructive",
    text: "text-destructive",
    bars: 4,
  },
};

export function PriorityIndicator({
  priority,
}: {
  priority: Priority;
}) {
  const cfg = PRIORITY_MAP[priority] ?? PRIORITY_MAP.medium;

  return (
    <div className="inline-flex items-center gap-2">
      <div className="flex items-end gap-0.5">
        {[1, 2, 3, 4].map((i) => (
          <span
            key={i}
            className={cn(
              "w-1 rounded-sm transition",
              i === 1 && "h-1.5",
              i === 2 && "h-2.5",
              i === 3 && "h-3.5",
              i === 4 && "h-4",
              i <= cfg.bars ? cfg.bar : "bg-muted"
            )}
          />
        ))}
      </div>
      <span className={cn("text-xs font-medium", cfg.text)}>
        {cfg.label}
      </span>
    </div>
  );
}