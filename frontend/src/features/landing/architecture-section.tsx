import { ArrowDown, GitBranch } from "lucide-react";

import { Card } from "@/components/ui/card";
import { architectureBranches } from "@/features/landing/data";
import { MotionDiv, MotionSection } from "@/features/landing/motion";

export function ArchitectureSection() {
  return (
    <MotionSection
      className="border-y border-white/[0.08] bg-white/[0.015] px-4 py-20 sm:px-6 lg:px-8"
      id="architecture"
      initial={{ opacity: 0 }}
      transition={{ duration: 0.55 }}
      viewport={{ once: true, margin: "-120px" }}
      whileInView={{ opacity: 1 }}
    >
      <div className="mx-auto grid max-w-7xl gap-10 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
        <div>
          <p className="mb-3 text-sm font-medium text-secondary">
            Architecture
          </p>
          <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            A workspace hub for programming and database learning.
          </h2>
          <p className="mt-5 max-w-xl text-sm leading-7 text-slate-400">
            CodeLens AI routes each learning experience through the right
            engine: deterministic Python analysis for code understanding and
            SemanticSQL for schema-aware query practice.
          </p>
        </div>

        <Card className="p-5 sm:p-6">
          <div className="grid gap-4">
            <div className="rounded-2xl border border-primary/30 bg-primary/10 p-4 text-center">
              <p className="text-xs font-medium uppercase tracking-[0.24em] text-primary">
                CodeLens AI
              </p>
              <p className="mt-2 text-lg font-semibold text-white">
                Workspace Hub
              </p>
            </div>

            <div className="flex justify-center text-slate-600">
              <ArrowDown className="size-5" />
            </div>

            <div className="grid gap-4 md:grid-cols-2">
              {architectureBranches.map((branch, branchIndex) => (
                <MotionDiv
                  className="rounded-2xl border border-white/[0.08] bg-[#07101F] p-4"
                  initial={{ opacity: 0, y: 18 }}
                  key={branch.workspace}
                  transition={{ duration: 0.45, delay: branchIndex * 0.1 }}
                  viewport={{ once: true }}
                  whileInView={{ opacity: 1, y: 0 }}
                >
                  <div className="mb-4 flex items-center gap-3">
                    <span className="grid size-9 place-items-center rounded-xl bg-secondary/10 text-secondary">
                      <GitBranch className="size-4" />
                    </span>
                    <h3 className="font-semibold text-white">
                      {branch.workspace}
                    </h3>
                  </div>
                  <div className="grid gap-3">
                    {branch.steps.map((step, index) => (
                      <div className="grid gap-3" key={step}>
                        <div className="flex items-center gap-3 rounded-xl border border-white/[0.08] bg-white/[0.03] p-3">
                          <span className="grid size-8 place-items-center rounded-lg bg-primary/15 font-mono text-[10px] text-primary">
                            0{index + 1}
                          </span>
                          <span className="text-sm font-medium text-slate-200">
                            {step}
                          </span>
                        </div>
                        {index < branch.steps.length - 1 && (
                          <div className="flex justify-center text-slate-700">
                            <ArrowDown className="size-4" />
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </MotionDiv>
              ))}
            </div>
          </div>
        </Card>
      </div>
    </MotionSection>
  );
}
