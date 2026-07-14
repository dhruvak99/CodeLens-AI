"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { motion } from "framer-motion";

import { EditorPanel } from "@/features/playground/components/editor-panel";
import { ExplanationDrawer } from "@/features/playground/components/explanation-drawer";
import { FindingsPanel } from "@/features/playground/components/findings-panel";
import { MetricsPanel } from "@/features/playground/components/metrics-panel";
import { PlaygroundNavbar } from "@/features/playground/components/playground-navbar";
import { RuntimePanel } from "@/features/playground/components/runtime-panel";
import { SemanticGraphPanel } from "@/features/playground/components/semantic-graph-panel";
import { sampleCode } from "@/features/playground/data";
import { useAnalyzeCode } from "@/features/playground/use-analyze-code";
import { applyFix, explainFinding } from "@/lib/api/client";
import type { AnalysisError, ExplainResponse, Finding } from "@/lib/api/contracts";

export function PlaygroundPage() {
  const [code, setCode] = useState(sampleCode);
  const [focusTarget, setFocusTarget] = useState<{
    line: number;
    nonce: number;
  } | null>(null);
  const [runtimeLine, setRuntimeLine] = useState<number | null>(null);
  const [applyingFindingId, setApplyingFindingId] = useState<string | null>(null);
  const [fixMessage, setFixMessage] = useState<{
    tone: "success" | "error";
    text: string;
  } | null>(null);
  const [explanationOpen, setExplanationOpen] = useState(false);
  const [explanation, setExplanation] = useState<ExplainResponse | null>(null);
  const [explainingId, setExplainingId] = useState<string | null>(null);
  const { analysis, error, hasAnalysis, isAnalyzing } = useAnalyzeCode(code);
  const hasAnalysisErrors = analysis.errors.length > 0;
  const hasSyntaxError = analysis.errors.some(
    (analysisError) => analysisError.type === "syntax_error"
  );

  const handleFindingClick = (finding: Finding) => {
    setFocusTarget({ line: finding.line, nonce: Date.now() });
  };

  const handleApplyFix = async (finding: Finding) => {
    if (!finding.codeAction || applyingFindingId !== null) {
      return;
    }

    setApplyingFindingId(finding.id);
    setFixMessage(null);

    try {
      const response = await applyFix({ code, findingId: finding.id });
      if (!response.applied) {
        setFixMessage({ tone: "error", text: response.message });
        return;
      }

      setCode(response.updatedCode);
      setFixMessage({ tone: "success", text: response.message });
    } catch {
      setFixMessage({ tone: "error", text: "Failed to apply fix." });
    } finally {
      setApplyingFindingId(null);
    }
  };

  const explainMutation = useMutation({
    mutationFn: explainFinding,
    onSuccess: (response) => {
      setExplanation(response);
      setExplanationOpen(true);
    },
    onError: () => {
      setExplanation({
        summary: "AI explanation unavailable.",
        rootCause: "AI explanation unavailable.",
        explanation: "AI explanation unavailable.",
        howToFix: "AI explanation unavailable.",
        correctedExample: "",
        learningTip: "AI explanation unavailable.",
        bestPractice: "AI explanation unavailable.",
        confidence: 0,
        unavailable: true
      });
      setExplanationOpen(true);
    },
    onSettled: () => {
      setExplainingId(null);
    }
  });

  const handleExplainFinding = (finding: Finding) => {
    setExplainingId(finding.id);
    setExplanationOpen(true);
    setExplanation(null);
    explainMutation.mutate({
      code,
      findingId: finding.id,
      finding,
      metrics: analysis.metrics
    });
  };

  const handleExplainError = (analysisError: AnalysisError, index: number) => {
    const explanationId = `syntax-${index}`;

    setExplainingId(explanationId);
    setExplanationOpen(true);
    setExplanation(null);
    explainMutation.mutate({
      code,
      findingId: explanationId,
      error: analysisError,
      metrics: analysis.metrics
    });
  };

  return (
    <main className="min-h-screen bg-background text-foreground">
      <PlaygroundNavbar fileName="binary_search.py" />
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
            runtimeLine={runtimeLine}
          />
          <FindingsPanel
            applyingFindingId={applyingFindingId}
            errors={analysis.errors}
            explainingId={explainingId}
            findings={analysis.findings}
            isAnalyzing={isAnalyzing}
            onApplyFix={handleApplyFix}
            onExplainError={handleExplainError}
            onExplainFinding={handleExplainFinding}
            onFindingClick={handleFindingClick}
          />
        </section>

        <section className="grid gap-3 xl:grid-cols-[1fr_1.25fr_1fr]">
          <SemanticGraphPanel
            graph={analysis.semanticGraph}
            isAnalyzing={isAnalyzing}
          />
          <RuntimePanel
            code={code}
            hasSyntaxError={hasSyntaxError}
            onCurrentLineChange={setRuntimeLine}
          />
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
              : "Live analysis runs 700ms after typing stops. Applied fixes re-analyze automatically."}
          </span>
          <span className="text-emerald-300">
            Runtime uses a restricted AST interpreter for v1.
          </span>
        </footer>
      </motion.div>
      {fixMessage ? (
        <div
          className={`fixed bottom-5 right-5 z-50 max-w-sm rounded-xl border px-4 py-3 text-sm shadow-2xl ${
            fixMessage.tone === "success"
              ? "border-emerald-400/30 bg-emerald-500/15 text-emerald-100"
              : "border-red-400/30 bg-red-500/15 text-red-100"
          }`}
        >
          {fixMessage.text}
        </div>
      ) : null}
      <ExplanationDrawer
        explanation={explanation}
        isLoading={explainMutation.isPending}
        isOpen={explanationOpen}
        onClose={() => setExplanationOpen(false)}
      />
    </main>
  );
}
