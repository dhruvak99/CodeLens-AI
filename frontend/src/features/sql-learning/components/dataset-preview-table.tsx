import { TableProperties } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { SqlScalar, SqlTablePreviewResponse } from "@/lib/api/sql-client";

type DatasetPreviewTableProps = {
  errorMessage?: string;
  isLoading: boolean;
  preview?: SqlTablePreviewResponse;
  tableName: string;
};

export function DatasetPreviewTable({
  errorMessage,
  isLoading,
  preview,
  tableName
}: DatasetPreviewTableProps) {
  const columns = preview?.columns ?? [];
  const rows = normalizeRows(columns, preview?.rows ?? []);

  return (
    <Card className="overflow-hidden">
      <div className="flex items-center gap-3 border-b border-white/[0.08] p-5">
        <span className="grid size-10 place-items-center rounded-xl border border-cyan-400/20 bg-cyan-400/10 text-cyan-200">
          <TableProperties className="size-5" />
        </span>
        <div>
          <h2 className="text-sm font-semibold text-white">Dataset Preview</h2>
          <p className="text-xs text-slate-500">First rows from {tableName || "the selected table"}.</p>
        </div>
      </div>

      {errorMessage ? (
        <StateMessage tone="error" message={errorMessage} />
      ) : isLoading ? (
        <StateMessage message="Loading table preview..." />
      ) : columns.length === 0 ? (
        <StateMessage message="Select a table to preview its rows." />
      ) : (
        <>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[760px] text-left text-sm">
          <thead className="bg-white/[0.03] text-xs uppercase tracking-[0.18em] text-slate-500">
            <tr>
              {columns.map((column) => (
                <th className="px-5 py-3 font-medium" key={column}>
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-white/[0.06] text-slate-300">
            {rows.map((row, index) => (
              <tr className="transition hover:bg-white/[0.03]" key={`${tableName}-${index}`}>
                {columns.map((column) => (
                  <td className="px-5 py-4" key={column}>
                    {formatCell(row[column])}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="border-t border-white/[0.08] px-5 py-3 text-xs text-slate-500">
        Showing first {rows.length} of {preview?.total_rows ?? rows.length} rows
      </div>
        </>
      )}
    </Card>
  );
}

function normalizeRows(
  columns: string[],
  rows: SqlTablePreviewResponse["rows"]
): Array<Record<string, SqlScalar>> {
  return rows.map((row) => {
    if (!Array.isArray(row)) {
      return row;
    }

    return columns.reduce<Record<string, SqlScalar>>((record, column, index) => {
      record[column] = row[index] ?? null;
      return record;
    }, {});
  });
}

function formatCell(value: SqlScalar | undefined) {
  if (value === null || value === undefined) {
    return "—";
  }

  return String(value);
}

function StateMessage({
  message,
  tone = "neutral"
}: {
  message: string;
  tone?: "neutral" | "error";
}) {
  return (
    <div
      className={`m-5 rounded-xl border p-4 text-sm ${
        tone === "error"
          ? "border-red-400/20 bg-red-500/10 text-red-100"
          : "border-white/[0.06] bg-slate-950/40 text-slate-400"
      }`}
    >
      {message}
    </div>
  );
}
