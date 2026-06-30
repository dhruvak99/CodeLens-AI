import { CheckCircle2, ChevronRight, Play, Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";
import { codeLines, findings } from "@/features/landing/data";
import { MotionDiv } from "@/features/landing/motion";
import { cn } from "@/lib/utils";

const toneStyles = {
  red: "border-red-400/40 bg-red-500/10 text-red-200",
  amber: "border-amber-400/40 bg-amber-500/10 text-amber-200",
  blue: "border-sky-400/40 bg-sky-500/10 text-sky-200"
};

export function HeroVisual() {
  return (
    <MotionDiv
      animate={{ y: 0, opacity: 1 }}
      className="relative mx-auto w-full max-w-6xl"
      initial={{ y: 36, opacity: 0 }}
      transition={{ duration: 0.7, delay: 0.18, ease: "easeOut" }}
    >
      <div className="absolute -inset-6 rounded-[2rem] bg-[radial-gradient(circle_at_20%_20%,rgba(124,58,237,0.22),transparent_34%),radial-gradient(circle_at_80%_60%,rgba(6,182,212,0.16),transparent_30%)] blur-2xl" />
      <Card
        className="relative overflow-hidden rounded-[1.35rem] bg-[#050B18]/95"
        id="playground-preview"
      >
        <div className="flex flex-col border-b border-white/[0.08] lg:flex-row">
          <div className="flex min-h-[420px] flex-1 flex-col">
            <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3">
              <div className="flex items-center gap-2">
                <span className="rounded-lg border border-white/[0.08] bg-white/[0.04] px-3 py-1.5 font-mono text-xs text-slate-200">
                  binary_search.py
                </span>
                <span className="hidden rounded-lg bg-white/[0.04] px-2 py-1 text-xs text-slate-500 sm:inline">
                  +
                </span>
              </div>
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <span>Python</span>
                <button className="inline-flex items-center gap-1 rounded-lg bg-primary px-3 py-1.5 text-white shadow-[0_0_22px_rgba(124,58,237,0.35)]">
                  <Play className="size-3" />
                  Run Analysis
                </button>
              </div>
            </div>

            <div className="grid flex-1 grid-cols-[44px_1fr] overflow-hidden font-mono text-[12px] leading-6 sm:text-[13px]">
              <div className="border-r border-white/[0.06] bg-white/[0.02] py-4 text-right text-slate-600">
                {codeLines.map((_, index) => (
                  <div className="pr-3" key={index}>
                    {index + 1}
                  </div>
                ))}
              </div>
              <pre className="overflow-x-auto py-4 text-slate-300">
                {codeLines.map((line, index) => (
                  <code
                    className={cn(
                      "block px-4",
                      index === 8 &&
                        "border-y border-primary/15 bg-primary/10 text-white"
                    )}
                    key={`${line}-${index}`}
                  >
                    <span className="text-slate-500">{line.slice(0, 4)}</span>
                    {line.slice(4)}
                  </code>
                ))}
              </pre>
            </div>

            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-white/[0.08] px-4 py-3 text-xs text-slate-400">
              <span className="inline-flex items-center gap-2 text-emerald-300">
                <CheckCircle2 className="size-4" />
                Analysis completed
              </span>
              <span>Ln 9, Col 21</span>
              <span>32ms</span>
            </div>
          </div>

          <aside className="w-full border-t border-white/[0.08] bg-white/[0.02] p-4 lg:w-[360px] lg:border-l lg:border-t-0">
            <div className="mb-4 flex items-center justify-between">
              <h3 className="text-sm font-semibold text-white">Findings</h3>
              <span className="rounded-md bg-primary/20 px-2 py-1 text-xs text-primary">
                3
              </span>
            </div>
            <div className="space-y-3">
              {findings.map((finding) => (
                <div
                  className="rounded-xl border border-white/[0.08] bg-[#0B1222] p-4"
                  key={finding.title}
                >
                  <div className="mb-2 flex items-center justify-between gap-3">
                    <p className="text-sm font-medium text-white">
                      {finding.title}
                    </p>
                    <span
                      className={cn(
                        "rounded-full border px-2 py-0.5 text-[10px]",
                        toneStyles[finding.tone as keyof typeof toneStyles]
                      )}
                    >
                      {finding.severity}
                    </span>
                  </div>
                  <p className="text-xs leading-5 text-slate-400">
                    {finding.detail}
                  </p>
                  <div className="mt-3 flex items-center justify-between">
                    <span className="text-xs text-slate-500">Line 6</span>
                    <button className="inline-flex items-center gap-1 rounded-lg border border-primary/30 px-2 py-1 text-xs text-primary">
                      <Sparkles className="size-3" />
                      Explain
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </aside>
        </div>

        <div className="grid border-t border-white/[0.08] md:grid-cols-3">
          {["Semantic Graph", "Runtime Trace", "Metrics"].map((label, index) => (
            <div
              className="min-h-28 border-white/[0.08] p-4 md:border-r md:last:border-r-0"
              key={label}
            >
              <div className="mb-3 flex items-center justify-between">
                <span className="text-xs font-medium text-white">{label}</span>
                <ChevronRight className="size-4 text-slate-600" />
              </div>
              {index === 0 && (
                <div className="flex h-16 items-center justify-center gap-3">
                  {["arr", "while", "if", "return"].map((node) => (
                    <span
                      className="rounded-full border border-primary/30 bg-primary/10 px-3 py-2 text-[10px] text-slate-200"
                      key={node}
                    >
                      {node}
                    </span>
                  ))}
                </div>
              )}
              {index === 1 && (
                <div className="space-y-2 font-mono text-[10px] text-slate-500">
                  <p>step 04 · mid = 4 · arr[mid] = 9</p>
                  <p className="text-red-300">step 05 · high = mid - 1</p>
                </div>
              )}
              {index === 2 && (
                <div className="grid grid-cols-2 gap-2 text-xs">
                  <span className="text-slate-500">Time</span>
                  <span className="text-emerald-300">O(log n)</span>
                  <span className="text-slate-500">Cyclomatic</span>
                  <span className="text-emerald-300">3</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </Card>
    </MotionDiv>
  );
}
