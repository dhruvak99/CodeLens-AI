import { Check, Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";
import { demoCode, demoFindings } from "@/features/landing/data";
import { MotionSection } from "@/features/landing/motion";

export function DemoSection() {
  return (
    <MotionSection
      className="px-4 py-20 sm:px-6 lg:px-8"
      id="docs"
      initial={{ opacity: 0, y: 24 }}
      transition={{ duration: 0.55 }}
      viewport={{ once: true, margin: "-120px" }}
      whileInView={{ opacity: 1, y: 0 }}
    >
      <div className="mx-auto max-w-7xl">
        <div className="mb-10 max-w-2xl">
          <p className="mb-3 text-sm font-medium text-secondary">Demo</p>
          <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Findings that stay close to the code.
          </h2>
        </div>

        <div className="grid gap-4 lg:grid-cols-[1.1fr_0.9fr]">
          <Card className="overflow-hidden">
            <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3">
              <span className="font-mono text-xs text-slate-300">
                score_window.py
              </span>
              <span className="rounded-md bg-emerald-500/10 px-2 py-1 text-xs text-emerald-300">
                analyzed
              </span>
            </div>
            <pre className="overflow-x-auto p-5 font-mono text-sm leading-7 text-slate-300">
              <code>{demoCode}</code>
            </pre>
          </Card>

          <Card className="p-5">
            <div className="mb-5 flex items-center gap-3">
              <span className="grid size-10 place-items-center rounded-xl bg-primary/15 text-primary">
                <Sparkles className="size-5" />
              </span>
              <div>
                <h3 className="font-semibold text-white">AI Findings</h3>
                <p className="text-sm text-slate-500">3 actionable insights</p>
              </div>
            </div>
            <div className="space-y-3">
              {demoFindings.map((finding) => (
                <div
                  className="flex gap-3 rounded-xl border border-white/[0.08] bg-white/[0.03] p-4"
                  key={finding}
                >
                  <Check className="mt-0.5 size-4 shrink-0 text-emerald-300" />
                  <p className="text-sm leading-6 text-slate-300">{finding}</p>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </MotionSection>
  );
}
