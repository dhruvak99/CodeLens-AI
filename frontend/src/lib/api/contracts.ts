export type Language = "python";
export type FindingSeverity = "low" | "medium" | "high";
export type FindingType =
  | "binary_search_logic_issue"
  | "dead_code"
  | "infinite_loop_risk"
  | "missing_base_case"
  | "missing_type_hints"
  | "undefined_variable"
  | "unreachable_code"
  | "unused_variable"
  | "unnecessary_else";
export type SemanticGraphNodeType =
  | "class"
  | "conditional"
  | "function"
  | "loop"
  | "variable"
  | "condition"
  | "return";

export interface SourceRange {
  startLine: number;
  startColumn: number;
  endLine: number;
  endColumn: number;
}

export interface CodeAction {
  title: string;
  description: string;
  range: SourceRange;
  replacement: string;
}

export interface AnalysisError {
  type: string;
  message: string;
  line?: number | null;
  column?: number | null;
}

export interface Finding {
  id: string;
  type: FindingType;
  severity: FindingSeverity;
  message: string;
  line: number;
  column: number;
  rule: string;
  codeAction?: CodeAction | null;
}

export interface SemanticGraphNode {
  id: string;
  label: string;
  type: SemanticGraphNodeType;
}

export interface SemanticGraphEdge {
  id: string;
  source: string;
  target: string;
  label: string;
}

export interface SemanticGraph {
  nodes: SemanticGraphNode[];
  edges: SemanticGraphEdge[];
}

export interface Metrics {
  timeComplexity: string;
  spaceComplexity: string;
  cyclomaticComplexity: number;
  functions: number;
  loops: number;
  linesOfCode: number;
  maintainabilityScore: number;
}

export interface AnalyzeRequest {
  code: string;
  language: Language;
}

export interface AnalyzeResponse {
  findings: Finding[];
  semanticGraph: SemanticGraph;
  metrics: Metrics;
  runtimeAvailable: boolean;
  errors: AnalysisError[];
}

export interface ExplainRequest {
  code: string;
  findingId: string;
}

export interface ExplainResponse {
  explanation: string;
}

export interface ApplyFixRequest {
  code: string;
  findingId: string;
}

export interface ApplyFixResponse {
  updatedCode: string;
  applied: boolean;
}

export interface RuntimeRequest {
  code: string;
}

export interface RuntimeStep {
  step: number;
  line?: number | null;
  statement: string;
}

export interface RuntimeVariable {
  name: string;
  value: string;
  step: number;
}

export interface RuntimeResponse {
  steps: RuntimeStep[];
  variables: RuntimeVariable[];
  callStack: string[];
}

export interface MetricsRequest {
  code: string;
}

export type MetricsResponse = Metrics;
