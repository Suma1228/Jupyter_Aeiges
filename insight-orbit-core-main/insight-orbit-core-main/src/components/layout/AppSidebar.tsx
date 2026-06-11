import { Link, useRouterState } from "@tanstack/react-router";
import {
  LayoutDashboard,
  FileText,
  BarChart3,
  Sparkles,
  Plus,
  ShieldCheck,
  type LucideIcon,
} from "lucide-react";
import { cn } from "@/lib/utils";

export type WorkspaceRole = "customer" | "ops";

interface NavItem {
  label: string;
  to: string;
  icon: LucideIcon;
}

const NAV: Record<WorkspaceRole, NavItem[]> = {
  customer: [
    { label: "Dashboard", to: "/customer", icon: LayoutDashboard },
    { label: "Complaints", to: "/customer/complaints", icon: FileText },
    { label: "Track Status", to: "/customer/track", icon: BarChart3 },
    { label: "AI Insights", to: "/customer/insights", icon: Sparkles },
  ],
  ops: [
    { label: "Dashboard", to: "/ops", icon: LayoutDashboard },
    { label: "Complaints", to: "/ops/complaints", icon: FileText },
    { label: "Analytics", to: "/ops/analytics", icon: BarChart3 },
    { label: "AI Insights", to: "/ops/insights", icon: Sparkles },
  ],
};

interface AppSidebarProps {
  role: WorkspaceRole;
}

export function AppSidebar({ role }: AppSidebarProps) {
  const pathname = useRouterState({ select: (s) => s.location.pathname });
  const items = NAV[role];

  return (
    <aside className="glass-strong sticky top-0 hidden h-screen w-64 shrink-0 flex-col p-4 lg:flex">
      <Link to="/" className="flex items-center gap-2.5 px-2 py-3">
        <div className="grid h-9 w-9 place-items-center rounded-xl bg-gradient-to-br from-primary to-accent glow-ring">
          <ShieldCheck className="h-5 w-5 text-primary-foreground" />
        </div>
        <div>
          <p className="font-display text-base font-semibold tracking-tight text-foreground">
            Aegis
          </p>
          <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
            {role === "ops" ? "Ops Console" : "Member Portal"}
          </p>
        </div>
      </Link>

      {role === "customer" && (
        <Link
          to="/customer/raise"
          className="mt-4 inline-flex items-center justify-center gap-2 rounded-xl bg-primary px-3 py-2.5 text-sm font-medium text-primary-foreground transition hover:opacity-90 glow-ring"
        >
          <Plus className="h-4 w-4" />
          Raise Complaint
        </Link>
      )}

      <nav className="mt-6 flex flex-col gap-1">
        <p className="px-3 pb-2 font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
          Navigate
        </p>
        {items.map((item) => {
          const active =
            pathname === item.to ||
            (item.to !== `/${role}` && pathname.startsWith(item.to));
          const Icon = item.icon;
          return (
            <Link
              key={item.to}
              to={item.to}
              className={cn(
                "group relative flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition",
                active
                  ? "bg-primary/10 text-foreground ring-1 ring-primary/30"
                  : "text-muted-foreground hover:bg-accent/40 hover:text-foreground",
              )}
            >
              {active && (
                <span className="absolute left-0 top-1/2 h-6 w-0.5 -translate-y-1/2 rounded-r-full bg-primary" />
              )}
              <Icon
                className={cn(
                  "h-4 w-4 transition",
                  active ? "text-primary" : "text-muted-foreground group-hover:text-foreground",
                )}
              />
              {item.label}
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto">
        <div className="glass rounded-xl p-3">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 animate-pulse rounded-full bg-success" />
            <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
              Systems nominal
            </p>
          </div>
          <p className="mt-1.5 text-xs text-muted-foreground">
            AI agents standing by. All services operational.
          </p>
        </div>
      </div>
    </aside>
  );
}
