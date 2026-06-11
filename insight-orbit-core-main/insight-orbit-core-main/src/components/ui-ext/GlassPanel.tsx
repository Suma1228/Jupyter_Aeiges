import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface GlassPanelProps {
  children: ReactNode;
  className?: string;
  variant?: "default" | "strong";
}

export function GlassPanel({ children, className, variant = "default" }: GlassPanelProps) {
  return (
    <div
      className={cn(
        variant === "strong" ? "glass-strong" : "glass",
        "rounded-2xl",
        className,
      )}
    >
      {children}
    </div>
  );
}
