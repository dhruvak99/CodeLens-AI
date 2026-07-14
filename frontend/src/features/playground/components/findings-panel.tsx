"use client";

import {
  AlertCircle,
  Bug,
  CheckCircle2,
  Sparkles,
  Wand2
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { PanelShell } from "@/features/playground/components/panel-shell";
import type { AnalysisError, Finding, FindingSeverity } from "@/lib/api/contracts";
import { cn } from "@/lib/utils";

const toneClasses = {
  high: "border-red-400/50 bg-red-500/10 text-red-200",
  medium: "border-amber-400/50 bg-amber-500/10 text-amber-200",
  low: "border-sky-400/50 bg-sky-500/10 text-sky-200"
};

const severityLabel: Record<FindingSeverity, string> = {
  high: "High",
  medium: "Medium",
  low: "Low"
};

type FindingsPanelProps = {
  findings: Finding[];
  errors: AnalysisError[];
  applyingFindingId: string | null;
  explainingId: string | null;
  isAnalyzing: boolean;
  onApplyFix: (finding: Finding) => void;
  onExplainError: (error: AnalysisError, index: number) => void;
  onExplainFinding: (finding: Finding) => void;
  onFindingClick: (finding: Finding) => void;
};

function formatFindingType(type: string) {
  return type
    .split("_")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function FindingsPanel({
  applyingFindingId,
  explainingId,
  findings,
  errors,
  isAnalyzing,
  onApplyFix,
  onExplainError,
  onExplainFinding,
  onFindingClick
}: FindingsPanelProps) {
  const issueCount = findings.length + errors.length;

  return (
    <PanelShell
      title="Findings"
      eyebrow="Problems"
      className="h-[520px] min-h-[420px] max-h-[760px] resize-y"
      actions={
        <span
          className={cn(
            "rounded-lg px-2 py-1 text-xs",
            isAnalyzing
              ? "bg-primary/20 text-primary"
              : "bg-white/[0.04] text-slate-300"
          )}
        >
          {isAnalyzing ? "Analyzing..." : issueCount}
        </span>
      }
      bodyClassName="overflow-y-auto p-4"
    >
      {isAnalyzing && issueCount === 0 ? (
        <div className="space-y-3">
          {[0, 1, 2].map((item) => (
            <div
              className="h-28 animate-pulse rounded-xl border border-white/[0.08] bg-white/[0.04]"
              key={item}
            />
          ))}
        </div>
      ) : issueCount === 0 ? (
        <div className="grid h-full place-items-center rounded-xl border border-dashed border-white/[0.12] p-6 text-center">
          <div>
            <CheckCircle2 className="mx-auto mb-3 size-8 text-emerald-300" />
            <p className="text-sm font-medium text-white">No findings</p>
            <p className="mt-1 text-xs text-slate-500">
              The current code passed the active analyzer rules.
            </p>
          </div>
        </div>
      ) : (
        <div className="space-y-3">
          {isAnalyzing ? (
            <div className="rounded-xl border border-primary/30 bg-primary/10 px-4 py-3 text-sm text-primary">
              Analyzing...
            </div>
          ) : null}
          {errors.map((error, index) => (
            <article
              className="rounded-xl border border-red-400/40 bg-red-500/10 p-4"
              key={`${error.type}-${error.line ?? "line"}-${index}`}
            >
              <div className="flex items-start gap-3">
                <Bug className="mt-0.5 size-5 shrink-0 text-red-300" />
                <div className="min-w-0">
                  <div className="mb-2 flex flex-wrap items-center gap-2">
                    <span className="rounded-full border border-red-400/50 bg-red-500/10 px-2 py-0.5 text-[10px] font-medium text-red-200">
                      Syntax Error
                    </span>
                    <span className="text-xs text-slate-400">
                      Line {error.line ?? "?"}, Column {error.column ?? "?"}
                    </span>
                  </div>
                  <p className="text-sm leading-6 text-red-100">{error.message}</p>
                  <div className="mt-4">
                    <Button
                      disabled={explainingId === `syntax-${index}`}
                      onClick={() => onExplainError(error, index)}
                      size="sm"
                      variant="secondary"
                    >
                      <Sparkles className="size-4" />
                      {explainingId === `syntax-${index}`
                        ? "Explaining..."
                        : "Explain"}
                    </Button>
                  </div>
                </div>
              </div>
            </article>
          ))}
          {findings.map((finding) => (
            <article
              className="w-full rounded-xl border border-white/[0.08] bg-[#07101F] p-4 text-left transition hover:border-white/[0.16] focus:outline-none focus:ring-2 focus:ring-primary/60"
              key={finding.id}
              onClick={() => onFindingClick(finding)}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  onFindingClick(finding);
                }
              }}
              role="button"
              tabIndex={0}
            >
              <div className="mb-3 flex items-start justify-between gap-3">
                <div className="flex min-w-0 gap-3">
                  <AlertCircle className="mt-0.5 size-5 shrink-0 text-primary" />
                  <div className="min-w-0">
                    <div className="mb-1 flex flex-wrap items-center gap-2">
                      <span
                        className={cn(
                          "rounded-full border px-2 py-0.5 text-[10px] font-medium",
                          toneClasses[finding.severity]
                        )}
                      >
                        {severityLabel[finding.severity]}
                      </span>
                      <span className="text-xs text-slate-500">
                        Line {finding.line}
                      </span>
                    </div>
                    <h3 className="text-sm font-semibold text-white">
                      {formatFindingType(finding.type)}
                    </h3>
                  </div>
                </div>
              </div>
              <p className="text-sm leading-6 text-slate-400">
                {finding.message}
              </p>
              <p className="mt-2 font-mono text-[11px] text-slate-600">
                {finding.rule}
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                <Button
                  disabled={explainingId === finding.id}
                  onClick={(event) => {
                    event.stopPropagation();
                    onExplainFinding(finding);
                  }}
                  size="sm"
                  variant="secondary"
                >
                  <Sparkles className="size-4" />
                  {explainingId === finding.id ? "Explaining..." : "Explain"}
                </Button>
                <Button
                  disabled={!finding.codeAction || applyingFindingId === finding.id}
                  onClick={(event) => {
                    event.stopPropagation();
                    onApplyFix(finding);
                  }}
                  size="sm"
                  variant={finding.codeAction ? "default" : "secondary"}
                >
                  <Wand2 className="size-4" />
                  {applyingFindingId === finding.id ? "Applying..." : "Apply Fix"}
                </Button>
              </div>
            </article>
          ))}
        </div>
      )}
    </PanelShell>
  );
}
