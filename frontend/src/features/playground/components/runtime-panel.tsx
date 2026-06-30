"use client";

import { Clock3, Cpu, GitBranch, Layers } from "lucide-react";

import { PanelShell } from "@/features/playground/components/panel-shell";

const runtimeFeatures = [
  { label: "Step-by-step execution", icon: GitBranch },
  { label: "Variable tracking", icon: Cpu },
  { label: "Execution timeline", icon: Clock3 },
  { label: "Memory visualization", icon: Layers }
];

export function RuntimePanel() {
  return (
    <PanelShell
      title="Runtime Engine"
      eyebrow="Coming in v2"
      className="h-[360px] min-h-[300px] max-h-[560px] resize-y"
      bodyClassName="overflow-y-auto p-4"
    >
      <div className="grid h-full place-items-center">
        <div className="w-full max-w-md rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5">
          <div className="mb-5">
            <div className="mb-3 grid size-11 place-items-center rounded-xl border border-primary/30 bg-primary/15 text-primary">
              <Clock3 className="size-5" />
            </div>
            <h3 className="text-base font-semibold text-white">
              Runtime execution is currently disabled.
            </h3>
            <p className="mt-2 text-sm leading-6 text-slate-400">
              CodeLens AI v2 will include interactive execution insight without
              running code in the v1 analyzer.
            </p>
          </div>

          <div className="grid gap-2">
            {runtimeFeatures.map((feature) => {
              const Icon = feature.icon;

              return (
                <div
                  className="flex items-center gap-3 rounded-xl border border-white/[0.08] bg-[#07101F] px-3 py-2.5 text-sm text-slate-300"
                  key={feature.label}
                >
                  <Icon className="size-4 text-cyan-300" />
                  {feature.label}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </PanelShell>
  );
}
