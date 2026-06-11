import { EmptyState } from "./EmptyState";
import { GlassPanel } from "./GlassPanel";
import { Inbox } from "lucide-react";
import { type ReactNode } from "react";

export interface Column<T> {
  key: keyof T | string;
  header: string;
  render?: (row: T) => ReactNode;
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  rows: T[];
  emptyTitle?: string;
  emptyDescription?: string;
  emptyAction?: ReactNode;
}

export function DataTable<T extends { id: string | number }>({
  columns,
  rows,
  emptyTitle = "No records yet",
  emptyDescription = "Records will appear here once the data source is connected.",
  emptyAction,
}: DataTableProps<T>) {
  if (rows.length === 0) {
    return (
      <GlassPanel>
        <EmptyState
          icon={Inbox}
          title={emptyTitle}
          description={emptyDescription}
          action={emptyAction}
        />
      </GlassPanel>
    );
  }

  return (
    <GlassPanel className="overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm">
          <thead>
            <tr className="border-b border-border bg-background/40">
              {columns.map((c) => (
                <th
                  key={String(c.key)}
                  className={`px-4 py-3 font-mono text-[11px] uppercase tracking-wider text-muted-foreground ${c.className ?? ""}`}
                >
                  {c.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.id}
                className="border-b border-border/50 transition hover:bg-accent/30"
              >
                {columns.map((c) => (
                  <td key={String(c.key)} className={`px-4 py-3 text-foreground ${c.className ?? ""}`}>
                    {c.render ? c.render(row) : String((row as Record<string, unknown>)[c.key as string] ?? "—")}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </GlassPanel>
  );
}
