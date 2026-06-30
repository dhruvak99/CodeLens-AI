"use client";

import { Activity, Loader2 } from "lucide-react";

import { PanelShell } from "@/features/playground/components/panel-shell";
import type { Metrics } from "@/lib/api/contracts";

type MetricsPanelProps = {
  metrics: Metrics | null;
  isAnalyzing: boolean;
};

function maintainabilityLabel(score: number | null) {
  if (score === null) {
    return "Unavailable";
  }
  if (score >= 8.5) {
    return "Excellent";
  }
  if (score >= 7) {
    return "Good";
  }
  if (score >= 5) {
    return "Fair";
  }
  return "Poor";
}

function formatValue(value: string | number | null) {
  return value === null ? "—" : String(value);
}

export function MetricsPanel({ metrics, isAnalyzing }: MetricsPanelProps) {
  const metricItems = [
    { label: "Time Complexity", value: metrics?.timeComplexity ?? null },
    { label: "Space Complexity", value: metrics?.spaceComplexity ?? null },
    {
      label: "Cyclomatic Complexity",
      value: metrics?.cyclomaticComplexity ?? null
    },
    { label: "Functions", value: metrics?.functions ?? null },
    { label: "Loops", value: metrics?.loops ?? null },
    { label: "LOC", value: metrics?.linesOfCode ?? null }
  ];
  const score = metrics?.maintainabilityScore ?? null;
  const scoreLabel = maintainabilityLabel(score);

  return (
    <PanelShell
      title="Metrics"
      eyebrow="Complexity"
      className="h-[360px] min-h-[300px] max-h-[560px] resize-y"
      bodyClassName="grid gap-5 p-4 lg:grid-cols-[1fr_140px]"
    >
      <div className="space-y-3">
        {isAnalyzing
          ? metricItems.map((metric) => (
              <div
                className="h-[46px] animate-pulse rounded-xl border border-white/[0.08] bg-white/[0.04]"
                key={metric.label}
              />
            ))
          : metricItems.map((metric) => (
              <div
                className="flex items-center justify-between gap-3 rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3"
                key={metric.label}
              >
                <span className="text-sm text-slate-400">{metric.label}</span>
                <span className="whitespace-nowrap font-mono text-sm font-medium text-emerald-300">
                  {formatValue(metric.value)}
                </span>
              </div>
            ))}
      </div>
      <div className="grid place-items-center rounded-2xl border border-white/[0.08] bg-[#07101F] p-4">
        <div className="relative grid size-28 place-items-center rounded-full border-[10px] border-slate-700 border-t-emerald-400 border-r-emerald-400">
          <div className="text-center">
            {isAnalyzing ? (
              <Loader2 className="mx-auto mb-2 size-5 animate-spin text-primary" />
            ) : (
              <Activity className="mx-auto mb-1 size-5 text-emerald-300" />
            )}
            <p className="text-2xl font-semibold text-white">
              {isAnalyzing ? "—" : formatValue(score)}
            </p>
            <p className="text-xs text-emerald-300">
              {isAnalyzing ? "Analyzing" : scoreLabel}
            </p>
          </div>
        </div>
      </div>
    </PanelShell>
  );
}
