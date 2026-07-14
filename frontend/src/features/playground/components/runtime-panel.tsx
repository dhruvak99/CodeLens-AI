"use client";

import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { useMutation } from "@tanstack/react-query";
import {
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  CircleStop,
  Play,
  RotateCcw,
  Terminal,
  Variable
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { PanelShell } from "@/features/playground/components/panel-shell";
import { getRuntimeTrace } from "@/lib/api/client";
import type { RuntimeResponse, RuntimeStep } from "@/lib/api/contracts";

interface RuntimePanelProps {
  code: string;
  hasSyntaxError: boolean;
  onCurrentLineChange: (line: number | null) => void;
}

const PLAYBACK_SPEED_MS = 700;

export function RuntimePanel({
  code,
  hasSyntaxError,
  onCurrentLineChange
}: RuntimePanelProps) {
  const [runtime, setRuntime] = useState<RuntimeResponse | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackFinished, setPlaybackFinished] = useState(false);

  const runtimeMutation = useMutation({
    mutationFn: getRuntimeTrace,
    onSuccess: (response) => {
      setRuntime(response);
      setCurrentIndex(0);
      setIsPlaying(false);
      setPlaybackFinished(false);
    },
    onError: () => {
      setRuntime({
        success: false,
        steps: [],
        output: [],
        error: {
          type: "RuntimeUnavailable",
          message: "Unable to reach the runtime engine."
        }
      });
      setCurrentIndex(0);
      setIsPlaying(false);
      setPlaybackFinished(false);
    }
  });

  const steps = runtime?.steps ?? [];
  const currentStep = steps[currentIndex] ?? null;
  const canStepBackward = currentIndex > 0;
  const canStepForward = currentIndex < steps.length - 1;
  const hasRunnableCode = code.trim().length > 0;
  const hasExecutableStatements =
    runtime?.success === true &&
    steps.some((step) => !step.executedStatement.trimStart().startsWith("def "));
  const isFunctionOnlyFile =
    runtime?.success === true && steps.length > 0 && !hasExecutableStatements;
  const disableRun = runtimeMutation.isPending || hasSyntaxError;
  const runTooltip = hasSyntaxError
    ? "Cannot execute code with syntax errors."
    : "Run runtime trace";

  const visibleOutput = useMemo(() => {
    if (currentStep) {
      return currentStep.output;
    }

    return runtime?.output ?? [];
  }, [currentStep, runtime?.output]);

  const variables = currentStep?.variables ?? {};

  useEffect(() => {
    if (!isPlaying) {
      return;
    }

    if (!canStepForward) {
      setIsPlaying(false);
      if (steps.length > 0) {
        setPlaybackFinished(true);
      }
      return;
    }

    const timer = window.setTimeout(() => {
      setCurrentIndex((index) => Math.min(index + 1, steps.length - 1));
    }, PLAYBACK_SPEED_MS);

    return () => window.clearTimeout(timer);
  }, [canStepForward, isPlaying, steps.length]);

  useEffect(() => {
    setRuntime(null);
    setCurrentIndex(0);
    setIsPlaying(false);
    setPlaybackFinished(false);
    onCurrentLineChange(null);
  }, [code, onCurrentLineChange]);

  useEffect(() => {
    onCurrentLineChange(isFunctionOnlyFile ? null : (currentStep?.line ?? null));
  }, [currentStep?.line, isFunctionOnlyFile, onCurrentLineChange]);

  const runRuntime = () => {
    if (hasSyntaxError) {
      return;
    }

    if (!hasRunnableCode) {
      setRuntime({
        success: false,
        steps: [],
        output: [],
        error: {
          type: "UnsupportedSyntax",
          message: "Enter Python code before running the runtime engine."
        }
      });
      setPlaybackFinished(false);
      return;
    }

    runtimeMutation.mutate({ code });
  };

  const resetRuntime = () => {
    setCurrentIndex(0);
    setIsPlaying(false);
    setPlaybackFinished(false);
  };

  const previousStep = () => {
    setPlaybackFinished(false);
    setCurrentIndex((index) => Math.max(index - 1, 0));
  };

  const nextStep = () => {
    setPlaybackFinished(false);
    setCurrentIndex((index) => Math.min(index + 1, steps.length - 1));
  };

  return (
    <PanelShell
      title="Runtime Engine"
      eyebrow={runtimeMutation.isPending ? "Executing" : "AST interpreter"}
      className="h-[360px] min-h-[300px] max-h-[560px] resize-y"
      bodyClassName="overflow-hidden p-0"
    >
      <div className="flex h-full flex-col">
        <div className="flex flex-wrap items-center gap-2 border-b border-white/[0.08] bg-white/[0.02] p-3">
          <Button
            className="h-8 gap-2 bg-primary px-3 text-xs text-white transition hover:bg-primary/90 disabled:cursor-not-allowed disabled:bg-white/[0.06] disabled:text-slate-500 disabled:shadow-none"
            disabled={disableRun}
            onClick={runRuntime}
            title={runTooltip}
            type="button"
          >
            <Play className="size-3.5" />
            Run
          </Button>
          <IconButton
            disabled={!canStepBackward}
            label="Previous step"
            onClick={previousStep}
          >
            <ChevronLeft className="size-4" />
          </IconButton>
          <IconButton
            disabled={!canStepForward}
            label="Next step"
            onClick={nextStep}
          >
            <ChevronRight className="size-4" />
          </IconButton>
          <IconButton
            disabled={isPlaying || steps.length <= 1 || !canStepForward}
            label="Play timeline"
            onClick={() => {
              setPlaybackFinished(false);
              setIsPlaying(true);
            }}
          >
            <Play className="size-4" />
          </IconButton>
          <IconButton
            disabled={!isPlaying}
            label="Pause timeline"
            onClick={() => setIsPlaying(false)}
          >
            <CircleStop className="size-4" />
          </IconButton>
          <IconButton
            disabled={steps.length === 0}
            label="Reset timeline"
            onClick={resetRuntime}
          >
            <RotateCcw className="size-4" />
          </IconButton>
          <div className="ml-auto text-xs text-slate-500">
            {playbackFinished
              ? "Execution Finished"
              : steps.length > 0
              ? `Step ${currentIndex + 1} of ${steps.length}`
              : "No execution yet"}
          </div>
        </div>
        {hasSyntaxError ? (
          <div className="border-b border-amber-300/20 bg-amber-400/10 px-4 py-2 text-xs text-amber-100">
            Cannot execute code with syntax errors.
          </div>
        ) : null}

        {runtimeMutation.isPending ? (
          <RuntimeStatus message="Executing restricted Python AST..." />
        ) : runtime?.error ? (
          <RuntimeErrorState error={runtime.error} />
        ) : isFunctionOnlyFile ? (
          <RuntimeStatus message={"No executable statements found.\n\nCall a function to execute it."} />
        ) : currentStep ? (
          <div className="grid min-h-0 flex-1 grid-cols-1 gap-0 lg:grid-cols-[1fr_0.9fr]">
            <ExecutionTimeline
              currentIndex={currentIndex}
              onSelectStep={setCurrentIndex}
              steps={steps}
            />
            <div className="grid min-h-0 grid-rows-[1fr_0.8fr] border-t border-white/[0.08] lg:border-l lg:border-t-0">
              <VariablesPanel
                changedVariable={currentStep.changedVariable}
                variables={variables}
              />
              <ConsolePanel output={visibleOutput} />
            </div>
          </div>
        ) : (
          <RuntimeStatus message="Run the current editor code to generate an execution timeline." />
        )}
      </div>
    </PanelShell>
  );
}

interface IconButtonProps {
  children: ReactNode;
  disabled: boolean;
  label: string;
  onClick: () => void;
}

function IconButton({ children, disabled, label, onClick }: IconButtonProps) {
  return (
    <Button
      aria-label={label}
      className="size-8 border-white/[0.08] bg-white/[0.03] p-0 text-slate-300 transition hover:bg-white/[0.08] disabled:cursor-not-allowed disabled:text-slate-600"
      disabled={disabled}
      onClick={onClick}
      title={label}
      type="button"
      variant="secondary"
    >
      {children}
    </Button>
  );
}

function RuntimeStatus({ message }: { message: string }) {
  return (
    <div className="grid flex-1 place-items-center p-5">
      <div className="max-w-sm text-center">
        <div className="mx-auto mb-3 grid size-11 place-items-center rounded-xl border border-primary/30 bg-primary/15 text-primary">
          <Terminal className="size-5" />
        </div>
        <p className="whitespace-pre-line text-sm leading-6 text-slate-400">
          {message}
        </p>
      </div>
    </div>
  );
}

function RuntimeErrorState({
  error
}: {
  error: NonNullable<RuntimeResponse["error"]>;
}) {
  return (
    <div className="grid flex-1 place-items-center p-5">
      <div className="w-full max-w-md rounded-xl border border-red-400/20 bg-red-500/10 p-4">
        <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-red-200">
          <AlertTriangle className="size-4" />
          {error.type}
        </div>
        <p className="text-sm leading-6 text-red-100/80">{error.message}</p>
        {error.line ? (
          <p className="mt-3 text-xs text-red-100/60">
            Line {error.line}
            {error.column !== null && error.column !== undefined
              ? `, column ${error.column}`
              : ""}
          </p>
        ) : null}
      </div>
    </div>
  );
}

function ExecutionTimeline({
  currentIndex,
  onSelectStep,
  steps
}: {
  currentIndex: number;
  onSelectStep: (index: number) => void;
  steps: RuntimeStep[];
}) {
  return (
    <div className="min-h-0 overflow-y-auto p-3">
      <div className="mb-2 text-xs font-medium uppercase tracking-[0.16em] text-slate-500">
        Execution Timeline
      </div>
      <div className="space-y-2">
        {steps.map((step, index) => {
          const isActive = index === currentIndex;

          return (
            <button
              className={`w-full rounded-xl border p-3 text-left transition ${
                isActive
                  ? "border-primary/50 bg-primary/15"
                  : "border-white/[0.08] bg-white/[0.03] hover:bg-white/[0.06]"
              }`}
              key={step.stepNumber}
              onClick={() => onSelectStep(index)}
              type="button"
            >
              <div className="mb-2 flex items-center justify-between gap-3">
                <span className="text-xs font-semibold text-slate-300">
                  Step {step.stepNumber}
                </span>
                <span className="rounded-full border border-white/[0.08] px-2 py-0.5 text-[11px] text-cyan-200">
                  Current line {step.line ?? "—"}
                </span>
              </div>
              <code className="block whitespace-pre-wrap break-words font-mono text-xs leading-5 text-slate-300">
                {step.executedStatement}
              </code>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function VariablesPanel({
  changedVariable,
  variables
}: {
  changedVariable?: string | null;
  variables: Record<string, string>;
}) {
  const entries = Object.entries(variables);

  return (
    <div className="min-h-0 overflow-y-auto border-b border-white/[0.08] p-3">
      <div className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.16em] text-slate-500">
        <Variable className="size-3.5" />
        Variables
      </div>
      {entries.length === 0 ? (
        <p className="text-sm text-slate-500">No variables in scope.</p>
      ) : (
        <div className="space-y-2">
          {entries.map(([name, value]) => {
            const changed = name === changedVariable;

            return (
              <div
                className={`flex items-center justify-between gap-3 rounded-lg border px-3 py-2 font-mono text-xs ${
                  changed
                    ? "border-cyan-300/40 bg-cyan-400/10 text-cyan-100"
                    : "border-white/[0.08] bg-white/[0.03] text-slate-300"
                }`}
                key={name}
              >
                <span>{name}</span>
                <span className="truncate text-right">{value}</span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function ConsolePanel({ output }: { output: string[] }) {
  const newestOutputIndex = output.length - 1;

  return (
    <div className="min-h-0 overflow-y-auto p-3">
      <div className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-[0.16em] text-slate-500">
        <Terminal className="size-3.5" />
        Console Output
      </div>
      {output.length === 0 ? (
        <p className="text-sm text-slate-500">No output captured.</p>
      ) : (
        <div className="space-y-1 rounded-xl border border-white/[0.08] bg-[#020617] p-3 font-mono text-xs leading-5 text-emerald-200">
          {output.map((line, index) => (
            <div
              className={
                index === newestOutputIndex
                  ? "rounded-md bg-emerald-400/10 px-2 py-1 text-emerald-100"
                  : "px-2 py-1"
              }
              key={`${line}-${index}`}
            >
              {line}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
