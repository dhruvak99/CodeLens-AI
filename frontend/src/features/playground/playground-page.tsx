"use client";

import { useState } from "react";
import { motion } from "framer-motion";

import { EditorPanel } from "@/features/playground/components/editor-panel";
import { FindingsPanel } from "@/features/playground/components/findings-panel";
import { MetricsPanel } from "@/features/playground/components/metrics-panel";
import { PlaygroundNavbar } from "@/features/playground/components/playground-navbar";
import { RuntimePanel } from "@/features/playground/components/runtime-panel";
import { SemanticGraphPanel } from "@/features/playground/components/semantic-graph-panel";
import { sampleCode } from "@/features/playground/data";
import { useAnalyzeCode } from "@/features/playground/use-analyze-code";
import type { Finding } from "@/lib/api/contracts";

export function PlaygroundPage() {
  const [code, setCode] = useState(sampleCode);
  const [focusTarget, setFocusTarget] = useState<{
    line: number;
    nonce: number;
  } | null>(null);
  const { analysis, error, hasAnalysis, isAnalyzing, refetch } =
    useAnalyzeCode(code);
  const hasAnalysisErrors = analysis.errors.length > 0;

  const runPreview = () => {
    void refetch();
  };

  const handleFindingClick = (finding: Finding) => {
    setFocusTarget({ line: finding.line, nonce: Date.now() });
  };

  return (
    <main className="min-h-screen bg-background text-foreground">
      <PlaygroundNavbar
        fileName="binary_search.py"
        isRunning={isAnalyzing}
        onRun={runPreview}
      />
      <motion.div
        animate={{ opacity: 1, y: 0 }}
        className="mx-auto flex max-w-[1800px] flex-col gap-3 p-3 sm:p-4 lg:p-5"
        initial={{ opacity: 0, y: 16 }}
        transition={{ duration: 0.45, ease: "easeOut" }}
      >
        <section className="grid gap-3 lg:grid-cols-[minmax(0,1.55fr)_minmax(360px,0.95fr)]">
          <EditorPanel
            code={code}
            focusTarget={focusTarget}
            isAnalyzing={isAnalyzing}
            onCodeChange={setCode}
          />
          <FindingsPanel
            errors={analysis.errors}
            findings={analysis.findings}
            isAnalyzing={isAnalyzing}
            onFindingClick={handleFindingClick}
          />
        </section>

        <section className="grid gap-3 xl:grid-cols-[1fr_1.25fr_1fr]">
          <SemanticGraphPanel
            graph={analysis.semanticGraph}
            isAnalyzing={isAnalyzing}
          />
          <RuntimePanel />
          <MetricsPanel
            isAnalyzing={isAnalyzing}
            metrics={
              isAnalyzing || !hasAnalysis || hasAnalysisErrors ? null : analysis.metrics
            }
          />
        </section>

        <footer className="flex flex-col gap-2 rounded-2xl border border-white/[0.08] bg-white/[0.03] px-4 py-3 text-xs text-slate-500 sm:flex-row sm:items-center sm:justify-between">
          <span>
            {error
              ? "Unable to reach the analyzer. Check that the FastAPI server is running."
              : "Live analysis runs 700ms after typing stops."}
          </span>
          <span className="text-emerald-300">
            Runtime, AI explain, apply fix, and real metrics remain disabled.
          </span>
        </footer>
      </motion.div>
    </main>
  );
}
