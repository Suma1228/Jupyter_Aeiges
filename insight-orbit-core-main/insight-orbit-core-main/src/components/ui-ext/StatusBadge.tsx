import { cn } from "@/lib/utils";

export type ComplaintStatus =
  | "new"
  | "in_review"
  | "in_progress"
  | "awaiting_customer"
  | "resolved"
  | "escalated"
  | "closed";

const STATUS_MAP: Record<ComplaintStatus, { label: string; className: string; dot: string }> = {
  new: {
    label: "New",
    className: "bg-info/10 text-info ring-info/30",
    dot: "bg-info",
  },
  in_review: {
    label: "In Review",
    className: "bg-primary/10 text-primary ring-primary/30",
    dot: "bg-primary",
  },
  in_progress: {
    label: "In Progress",
    className: "bg-primary/10 text-primary ring-primary/30",
    dot: "bg-primary animate-pulse",
  },
  awaiting_customer: {
    label: "Awaiting Customer",
    className: "bg-warning/10 text-warning ring-warning/30",
    dot: "bg-warning",
  },
  resolved: {
    label: "Resolved",
    className: "bg-success/10 text-success ring-success/30",
    dot: "bg-success",
  },
  escalated: {
    label: "Escalated",
    className: "bg-destructive/10 text-destructive ring-destructive/30",
    dot: "bg-destructive animate-pulse",
  },
  closed: {
    label: "Closed",
    className: "bg-muted text-muted-foreground ring-border",
    dot: "bg-muted-foreground",
  },
};

export function StatusBadge({ status }: { status: ComplaintStatus }) {
  const cfg = STATUS_MAP[status] ?? STATUS_MAP.new;
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ring-1",
        cfg.className,
      )}
    >
      <span className={cn("h-1.5 w-1.5 rounded-full", cfg.dot)} />
      {cfg.label}
    </span>
  );
}
