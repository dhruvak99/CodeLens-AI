"use client";

import { keepPreviousData, useQuery } from "@tanstack/react-query";

import { analyzeCode } from "@/lib/api/client";
import type { AnalyzeResponse } from "@/lib/api/contracts";
import { useDebouncedValue } from "@/features/playground/use-debounced-value";

const EMPTY_ANALYSIS: AnalyzeResponse = {
  findings: [],
  semanticGraph: {
    nodes: [],
    edges: []
  },
  metrics: {
    timeComplexity: "O(1)",
    spaceComplexity: "O(1)",
    cyclomaticComplexity: 1,
    functions: 0,
    loops: 0,
    linesOfCode: 0,
    maintainabilityScore: 10
  },
  runtimeAvailable: false,
  errors: []
};

export function useAnalyzeCode(code: string) {
  const debouncedCode = useDebouncedValue(code, 700);

  const query = useQuery({
    queryKey: ["analyze", debouncedCode],
    queryFn: ({ signal }) =>
      analyzeCode({ code: debouncedCode, language: "python" }, signal),
    placeholderData: keepPreviousData,
    refetchOnMount: false
  });

  return {
    ...query,
    debouncedCode,
    analysis: query.data ?? EMPTY_ANALYSIS,
    hasAnalysis: query.data !== undefined,
    isAnalyzing: query.isFetching
  };
}
