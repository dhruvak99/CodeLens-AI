"use client";

import { Loader2, Sparkles, X } from "lucide-react";

import { Button } from "@/components/ui/button";
import type { ExplainResponse } from "@/lib/api/contracts";

type ExplanationDrawerProps = {
  explanation: ExplainResponse | null;
  isOpen: boolean;
  isLoading: boolean;
  onClose: () => void;
};

const sections: Array<{
  key: keyof Pick<
    ExplainResponse,
    | "rootCause"
    | "explanation"
    | "howToFix"
    | "correctedExample"
    | "learningTip"
    | "bestPractice"
  >;
  label: string;
}> = [
  { key: "rootCause", label: "Root Cause" },
  { key: "explanation", label: "Detailed Explanation" },
  { key: "howToFix", label: "How To Fix" },
  { key: "correctedExample", label: "Corrected Example" },
  { key: "learningTip", label: "Learning Tip" },
  { key: "bestPractice", label: "Best Practice" }
];

export function ExplanationDrawer({
  explanation,
  isLoading,
  isOpen,
  onClose
}: ExplanationDrawerProps) {
  if (!isOpen) {
    return null;
  }

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/45 backdrop-blur-sm">
      <button
        aria-label="Close explanation"
        className="absolute inset-0 cursor-default"
        onClick={onClose}
        type="button"
      />
      <aside className="relative flex h-full w-full max-w-xl flex-col border-l border-white/[0.08] bg-card shadow-2xl">
        <header className="flex h-16 items-center justify-between gap-3 border-b border-white/[0.08] px-5">
          <div className="min-w-0">
            <div className="flex items-center gap-2 text-sm font-semibold text-white">
              <Sparkles className="size-4 text-primary" />
              Issue Summary
            </div>
            <p className="mt-1 truncate text-xs text-slate-500">
              AI tutor explanation from existing analyzer output
            </p>
          </div>
          <Button
            aria-label="Close explanation"
            className="size-9 p-0"
            onClick={onClose}
            type="button"
            variant="secondary"
          >
            <X className="size-4" />
          </Button>
        </header>

        {isLoading ? (
          <div className="grid flex-1 place-items-center p-8 text-center">
            <div>
              <Loader2 className="mx-auto mb-3 size-7 animate-spin text-primary" />
              <p className="text-sm text-slate-300">
                Generating explanation with local Ollama...
              </p>
            </div>
          </div>
        ) : explanation ? (
          <div className="min-h-0 flex-1 overflow-y-auto p-5">
            <div
              className={`mb-4 rounded-xl border p-4 ${
                explanation.unavailable
                  ? "border-amber-300/30 bg-amber-400/10"
                  : "border-primary/25 bg-primary/10"
              }`}
            >
              <p className="text-sm leading-6 text-white">
                {explanation.summary}
              </p>
            </div>

            <div className="space-y-3">
              {sections.map((section) => {
                const value = explanation[section.key];
                if (!value) {
                  return null;
                }

                return (
                  <section
                    className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-4"
                    key={section.key}
                  >
                    <h3 className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                      {section.label}
                    </h3>
                    {section.key === "correctedExample" ? (
                      <pre className="overflow-x-auto whitespace-pre-wrap rounded-lg border border-white/[0.08] bg-[#020617] p-3 font-mono text-xs leading-5 text-cyan-100">
                        {value}
                      </pre>
                    ) : (
                      <p className="text-sm leading-6 text-slate-300">{value}</p>
                    )}
                  </section>
                );
              })}
            </div>

            <div className="mt-4 rounded-xl border border-white/[0.08] bg-white/[0.03] p-4">
              <h3 className="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">
                Confidence
              </h3>
              <div className="flex items-center gap-3">
                <div className="h-2 flex-1 overflow-hidden rounded-full bg-white/[0.08]">
                  <div
                    className="h-full rounded-full bg-primary"
                    style={{
                      width: `${Math.round(explanation.confidence * 100)}%`
                    }}
                  />
                </div>
                <span className="font-mono text-xs text-slate-300">
                  {Math.round(explanation.confidence * 100)}%
                </span>
              </div>
            </div>
          </div>
        ) : (
          <div className="grid flex-1 place-items-center p-8 text-center text-sm text-slate-400">
            Select Explain on a finding to open an AI tutor explanation.
          </div>
        )}
      </aside>
    </div>
  );
}

