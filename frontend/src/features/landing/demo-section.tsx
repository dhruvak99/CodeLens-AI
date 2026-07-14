import { Check, Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";
import { demoFindings, sqlDemoSteps } from "@/features/landing/data";
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
          <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Two guided learning loops.
          </h2>
        </div>

        <div className="grid gap-4 lg:grid-cols-2">
          <Card className="overflow-hidden">
            <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3">
              <span className="font-mono text-xs text-slate-300">
                Python Lab
              </span>
              <span className="rounded-md bg-emerald-500/10 px-2 py-1 text-xs text-emerald-300">
                Binary Search
              </span>
            </div>
            <div className="p-5">
              <div className="mb-5 flex items-center gap-3">
                <span className="grid size-10 place-items-center rounded-xl bg-primary/15 text-primary">
                  <Sparkles className="size-5" />
                </span>
                <div>
                  <h3 className="font-semibold text-white">Binary Search</h3>
                  <p className="text-sm text-slate-500">
                    Understand algorithm behavior step by step.
                  </p>
                </div>
              </div>
              <DemoSteps steps={demoFindings} />
            </div>
          </Card>

          <Card className="p-5">
            <div className="mb-5 flex items-center gap-3">
              <span className="grid size-10 place-items-center rounded-xl bg-primary/15 text-primary">
                <Sparkles className="size-5" />
              </span>
              <div>
                <h3 className="font-semibold text-white">SQL Lab</h3>
                <p className="text-sm text-slate-500">
                  Natural language to validated SQL tutoring.
                </p>
              </div>
            </div>
            <DemoSteps steps={sqlDemoSteps} />
          </Card>
        </div>
      </div>
    </MotionSection>
  );
}

function DemoSteps({ steps }: { steps: string[] }) {
  return (
    <div className="space-y-3">
      {steps.map((step, index) => (
        <div
          className="flex gap-3 rounded-xl border border-white/[0.08] bg-white/[0.03] p-4"
          key={step}
        >
          <Check className="mt-0.5 size-4 shrink-0 text-emerald-300" />
          <p className="text-sm leading-6 text-slate-300">{step}</p>
          {index < steps.length - 1 && (
            <span className="ml-auto font-mono text-xs text-slate-600">↓</span>
          )}
        </div>
      ))}
    </div>
  );
}
