import type {
  AnalyzeRequest,
  AnalyzeResponse,
  ApplyFixRequest,
  ApplyFixResponse,
  ExplainRequest,
  ExplainResponse,
  MetricsRequest,
  MetricsResponse,
  RuntimeRequest,
  RuntimeResponse
} from "@/lib/api/contracts";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_CODELENS_API ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "";

async function postJson<TRequest, TResponse>(
  path: string,
  payload: TRequest,
  signal?: AbortSignal
): Promise<TResponse> {
  const baseUrl = API_BASE_URL.replace(/\/$/, "");
  const response = await fetch(`${baseUrl}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload),
    signal
  });

  if (!response.ok) {
    throw new Error(`CodeLens API request failed: ${response.status}`);
  }

  return response.json() as Promise<TResponse>;
}

export function analyzeCode(
  payload: AnalyzeRequest,
  signal?: AbortSignal
): Promise<AnalyzeResponse> {
  return postJson<AnalyzeRequest, AnalyzeResponse>("/analyze", payload, signal);
}

export function explainFinding(
  payload: ExplainRequest
): Promise<ExplainResponse> {
  return postJson<ExplainRequest, ExplainResponse>("/explain", payload);
}

export function applyFix(
  payload: ApplyFixRequest
): Promise<ApplyFixResponse> {
  return postJson<ApplyFixRequest, ApplyFixResponse>("/apply-fix", payload);
}

export function getRuntimeTrace(
  payload: RuntimeRequest
): Promise<RuntimeResponse> {
  return postJson<RuntimeRequest, RuntimeResponse>("/runtime", payload);
}

export function getMetrics(
  payload: MetricsRequest
): Promise<MetricsResponse> {
  return postJson<MetricsRequest, MetricsResponse>("/metrics", payload);
}
