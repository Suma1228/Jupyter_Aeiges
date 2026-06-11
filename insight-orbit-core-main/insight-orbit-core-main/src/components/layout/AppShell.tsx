import { type ReactNode } from "react";
import { Link } from "@tanstack/react-router";
import { Bell, Search, UserCircle2 } from "lucide-react";
import { AppSidebar, type WorkspaceRole } from "./AppSidebar";

interface AppShellProps {
  role: WorkspaceRole;
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
}

export function AppShell({ role, title, subtitle, actions, children }: AppShellProps) {
  return (
    <div className="flex min-h-screen w-full">
      <AppSidebar role={role} />

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="glass sticky top-0 z-20 flex items-center gap-4 border-b border-border px-5 py-3 lg:px-8">
          <div className="min-w-0 flex-1">
            <p className="font-mono text-[10px] uppercase tracking-[0.22em] text-muted-foreground">
              {role === "ops" ? "Operations / " : "Member / "}
              <span className="text-primary">{title}</span>
            </p>
            <h1 className="mt-0.5 truncate text-xl font-semibold tracking-tight text-foreground">
              {title}
            </h1>
            {subtitle && (
              <p className="mt-0.5 truncate text-xs text-muted-foreground">{subtitle}</p>
            )}
          </div>

          <div className="hidden items-center gap-2 md:flex">
            <div className="glass flex w-72 items-center gap-2 rounded-xl px-3 py-2">
              <Search className="h-4 w-4 text-muted-foreground" />
              <input
                className="w-full bg-transparent text-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
                placeholder="Search complaints, customers, policies…"
              />
              <kbd className="rounded bg-muted px-1.5 py-0.5 font-mono text-[10px] text-muted-foreground">
                ⌘K
              </kbd>
            </div>
          </div>

          <div className="flex items-center gap-2">
            {actions}
            <button
              className="glass relative grid h-9 w-9 place-items-center rounded-xl text-muted-foreground transition hover:text-foreground"
              aria-label="Notifications"
            >
              <Bell className="h-4 w-4" />
              <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-primary" />
            </button>
            <Link
              to="/login"
              className="glass grid h-9 w-9 place-items-center rounded-xl text-muted-foreground transition hover:text-foreground"
              aria-label="Account"
            >
              <UserCircle2 className="h-4 w-4" />
            </Link>
          </div>
        </header>

        <main className="flex-1 px-5 py-6 lg:px-8 lg:py-8">{children}</main>
      </div>
    </div>
  );
}
