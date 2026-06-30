import { ArrowDown } from "lucide-react";

import { Card } from "@/components/ui/card";
import { architectureSteps } from "@/features/landing/data";
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
            A focused pipeline from editor signal to explainable insight.
          </h2>
          <p className="mt-5 max-w-xl text-sm leading-7 text-slate-400">
            The landing page mirrors the product architecture: editor input
            flows into the analysis engine, becomes a semantic graph, surfaces
            findings, and then turns those findings into AI explanations.
          </p>
        </div>

        <Card className="p-5 sm:p-6">
          <div className="grid gap-3">
            {architectureSteps.map((step, index) => (
              <MotionDiv
                className="grid gap-3"
                initial={{ opacity: 0, x: 18 }}
                key={step}
                transition={{ duration: 0.4, delay: index * 0.08 }}
                viewport={{ once: true }}
                whileInView={{ opacity: 1, x: 0 }}
              >
                <div className="flex items-center gap-4 rounded-2xl border border-white/[0.08] bg-[#07101F] p-4">
                  <span className="grid size-9 place-items-center rounded-xl bg-primary/15 font-mono text-xs text-primary">
                    0{index + 1}
                  </span>
                  <span className="font-medium text-white">{step}</span>
                </div>
                {index < architectureSteps.length - 1 && (
                  <div className="flex justify-center text-slate-600">
                    <ArrowDown className="size-5" />
                  </div>
                )}
              </MotionDiv>
            ))}
          </div>
        </Card>
      </div>
    </MotionSection>
  );
}
