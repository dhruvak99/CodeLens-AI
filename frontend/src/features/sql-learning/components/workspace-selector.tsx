"use client";

import { ChevronDown } from "lucide-react";

import { cn } from "@/lib/utils";

export type WorkspaceId = "python" | "sql";

const workspaceOptions: Array<{ id: WorkspaceId; label: string }> = [
  { id: "python", label: "Python Lab" },
  { id: "sql", label: "SQL Lab" }
];

type WorkspaceSelectorProps = {
  activeWorkspace: WorkspaceId;
  className?: string;
  onWorkspaceChange: (workspace: WorkspaceId) => void;
};

export function WorkspaceSelector({
  activeWorkspace,
  className,
  onWorkspaceChange
}: WorkspaceSelectorProps) {
  return (
    <div
      className={cn(
        "inline-flex max-w-full items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.04] px-3 py-2 text-xs text-slate-200 shadow-[0_12px_40px_rgba(0,0,0,0.18)]",
        className
      )}
    >
      <span className="hidden whitespace-nowrap text-slate-500 sm:inline">
        Workspace
      </span>
      <span aria-hidden="true" className="hidden text-slate-600 sm:inline">
        /
      </span>
      <div className="relative min-w-0">
        <select
          aria-label="Workspace"
          className="w-full appearance-none bg-transparent py-0 pl-0 pr-6 font-medium text-slate-100 outline-none transition hover:text-white"
          onChange={(event) =>
            onWorkspaceChange(event.target.value as WorkspaceId)
          }
          value={activeWorkspace}
        >
          {workspaceOptions.map((workspace) => (
            <option
              className="bg-slate-950 text-slate-100"
              key={workspace.id}
              value={workspace.id}
            >
              {workspace.label}
            </option>
          ))}
        </select>
        <ChevronDown className="pointer-events-none absolute right-0 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
      </div>
    </div>
  );
}
