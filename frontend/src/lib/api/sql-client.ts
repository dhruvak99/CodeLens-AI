export type SqlScalar = string | number | boolean | null;

export type SqlTableSummary = {
  name: string;
  row_count?: number;
  rowCount?: number;
  column_count?: number;
  columnCount?: number;
};

export type SqlTablesResponse = {
  tables: SqlTableSummary[];
};

export type SqlTablePreviewResponse = {
  table_name: string;
  columns: string[];
  rows: SqlScalar[][] | Array<Record<string, SqlScalar>>;
  total_rows?: number;
  page?: number;
  page_size?: number;
};

export type SqlSchemaColumn = {
  name: string;
  type: string;
  primary_key?: boolean;
  nullable?: boolean;
  not_null?: boolean;
};

export type SqlSchemaTable = {
  name: string;
  column_count?: number;
  columns: SqlSchemaColumn[];
};

export type SqlSchemaResponse = {
  table_count?: number;
  column_count?: number;
  tables: SqlSchemaTable[];
};

export type SqlQueryProcessRequest = {
  query: string;
  selected_table?: string;
  mode?: "learning" | string;
};

export type SqlValidationPayload = {
  valid: boolean;
  errors: string[];
};

export type SqlQueryProcessResponse = {
  generation_mode: string;
  generated_sql: string;
  corrected_sql?: string | null;
  executed_sql?: string | null;
  explanation?: string | null;
  validation: SqlValidationPayload;
  cache_hit: boolean;
  similarity_score: number;
  validation_status: string;
  validation_errors: string[];
  execution_time: number;
  rows_returned: number;
  results: Array<Record<string, SqlScalar>>;
};

const SQL_API_BASE_URL =
  process.env.NEXT_PUBLIC_SQL_API ?? "http://localhost:8001";

async function getJson<TResponse>(
  path: string,
  signal?: AbortSignal
): Promise<TResponse> {
  const response = await fetch(`${SQL_API_BASE_URL.replace(/\/$/, "")}${path}`, {
    signal
  });

  if (!response.ok) {
    throw new Error(`SemanticSQL request failed: ${response.status}`);
  }

  return response.json() as Promise<TResponse>;
}

async function postJson<TRequest, TResponse>(
  path: string,
  payload: TRequest
): Promise<TResponse> {
  const response = await fetch(`${SQL_API_BASE_URL.replace(/\/$/, "")}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`SemanticSQL request failed: ${response.status}`);
  }

  return response.json() as Promise<TResponse>;
}

export function getSqlTables(signal?: AbortSignal): Promise<SqlTablesResponse> {
  return getJson<SqlTablesResponse>("/api/v1/database/tables", signal);
}

export function getSqlTablePreview(
  tableName: string,
  signal?: AbortSignal
): Promise<SqlTablePreviewResponse> {
  return getJson<SqlTablePreviewResponse>(
    `/api/v1/database/table/${encodeURIComponent(tableName)}?page=1&page_size=10`,
    signal
  );
}

export function getSqlSchema(signal?: AbortSignal): Promise<SqlSchemaResponse> {
  return getJson<SqlSchemaResponse>("/api/v1/schema/", signal);
}

export function processSqlQuery(
  payload: SqlQueryProcessRequest
): Promise<SqlQueryProcessResponse> {
  return postJson<SqlQueryProcessRequest, SqlQueryProcessResponse>(
    "/api/v1/query/process",
    payload
  );
}
