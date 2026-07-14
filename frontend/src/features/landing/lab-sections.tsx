import { ArrowRight } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { PythonShowcase, SqlShowcase } from "@/features/landing/hero-visual";
import { MotionDiv, MotionSection } from "@/features/landing/motion";

export function PythonLabSection() {
  return (
    <MotionSection
      className="px-4 py-20 sm:px-6 lg:px-8"
      id="workspaces"
      initial={{ opacity: 0, y: 24 }}
      transition={{ duration: 0.55 }}
      viewport={{ once: true, margin: "-120px" }}
      whileInView={{ opacity: 1, y: 0 }}
    >
      <div className="mx-auto max-w-7xl">
        <LabHeader
          buttonLabel="Open Python Lab"
          description="Learn Python through semantic analysis, runtime execution, AI explanations, and interactive debugging."
          href="/playground?workspace=python"
          title="Python Lab"
        />
        <MotionDiv
          initial={{ opacity: 0, y: 24 }}
          transition={{ duration: 0.55, delay: 0.08 }}
          viewport={{ once: true }}
          whileInView={{ opacity: 1, y: 0 }}
        >
          <PythonShowcase />
        </MotionDiv>
      </div>
    </MotionSection>
  );
}

export function SqlLabSection() {
  return (
    <MotionSection
      className="border-y border-white/[0.08] bg-white/[0.015] px-4 py-20 sm:px-6 lg:px-8"
      id="sql-lab"
      initial={{ opacity: 0, y: 24 }}
      transition={{ duration: 0.55 }}
      viewport={{ once: true, margin: "-120px" }}
      whileInView={{ opacity: 1, y: 0 }}
    >
      <div className="mx-auto max-w-7xl">
        <LabHeader
          buttonLabel="Open SQL Lab"
          description="Learn SQL using natural language, schema exploration, validation, live execution, and AI tutoring."
          href="/playground?workspace=sql"
          title="SQL Lab"
        />
        <MotionDiv
          initial={{ opacity: 0, y: 24 }}
          transition={{ duration: 0.55, delay: 0.08 }}
          viewport={{ once: true }}
          whileInView={{ opacity: 1, y: 0 }}
        >
          <SqlShowcase />
        </MotionDiv>
      </div>
    </MotionSection>
  );
}

function LabHeader({
  buttonLabel,
  description,
  href,
  title
}: {
  buttonLabel: string;
  description: string;
  href: string;
  title: string;
}) {
  return (
    <div className="mb-10 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
      <div className="max-w-3xl">
        <p className="mb-3 text-sm font-medium text-secondary">Workspace</p>
        <h2 className="text-3xl font-semibold tracking-tight text-white sm:text-4xl">
          {title}
        </h2>
        <p className="mt-4 text-sm leading-7 text-slate-400 sm:text-base">
          {description}
        </p>
      </div>
      <Button asChild size="lg">
        <Link href={href}>
          {buttonLabel}
          <ArrowRight className="size-4" />
        </Link>
      </Button>
    </div>
  );
}
