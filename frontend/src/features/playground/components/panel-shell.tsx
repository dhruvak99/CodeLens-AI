import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

type PanelShellProps = {
  title: string;
  eyebrow?: string;
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
  bodyClassName?: string;
};

export function PanelShell({
  title,
  eyebrow,
  actions,
  children,
  className,
  bodyClassName
}: PanelShellProps) {
  return (
    <section
      className={cn(
        "flex min-h-0 flex-col overflow-hidden rounded-2xl border border-white/[0.08] bg-card/90 shadow-[0_18px_80px_rgba(0,0,0,0.24)]",
        className
      )}
    >
      <header className="flex h-14 shrink-0 items-center justify-between gap-3 border-b border-white/[0.08] px-4">
        <div className="min-w-0">
          <h2 className="truncate text-sm font-semibold text-white">{title}</h2>
          {eyebrow ? (
            <p className="mt-0.5 truncate text-xs text-slate-500">{eyebrow}</p>
          ) : null}
        </div>
        {actions ? <div className="flex shrink-0 items-center gap-2">{actions}</div> : null}
      </header>
      <div className={cn("min-h-0 flex-1", bodyClassName)}>{children}</div>
    </section>
  );
}
