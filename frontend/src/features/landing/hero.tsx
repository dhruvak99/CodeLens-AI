import { ArrowRight, GitBranch, PlayCircle } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { HeroVisual } from "@/features/landing/hero-visual";
import { MotionDiv, MotionSection } from "@/features/landing/motion";

export function Hero() {
  return (
    <MotionSection
      className="relative overflow-hidden px-4 pb-16 pt-32 sm:px-6 lg:px-8"
      id="top"
    >
      <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.035)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.035)_1px,transparent_1px)] bg-[size:80px_80px] opacity-30" />
      <div className="absolute inset-x-0 top-0 h-80 bg-[radial-gradient(circle_at_50%_0%,rgba(124,58,237,0.22),transparent_48%)]" />

      <div className="relative mx-auto max-w-7xl">
        <MotionDiv
          animate={{ y: 0, opacity: 1 }}
          className="mx-auto max-w-4xl text-center"
          initial={{ y: 24, opacity: 0 }}
          transition={{ duration: 0.65, ease: "easeOut" }}
        >
          <div className="mx-auto mb-6 inline-flex items-center gap-2 rounded-full border border-white/[0.08] bg-white/[0.04] px-4 py-2 text-sm text-slate-300">
            <GitBranch className="size-4 text-secondary" />
            Real-time semantic code intelligence
          </div>
          <h1 className="text-balance text-5xl font-semibold tracking-tight text-white sm:text-6xl lg:text-7xl">
            Understand Code Beyond Syntax.
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-pretty text-lg leading-8 text-slate-300">
            Real-time semantic analysis, execution visualization, and
            AI-powered code intelligence.
          </p>
          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Button asChild size="lg">
              <Link href="/playground">
                Open Playground
                <ArrowRight className="size-4" />
              </Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <a href="#architecture">
                <PlayCircle className="size-4" />
                View Architecture
              </a>
            </Button>
          </div>
        </MotionDiv>

        <div className="mt-16">
          <HeroVisual />
        </div>
      </div>
    </MotionSection>
  );
}
