import { Table2 } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { SqlScalar } from "@/lib/api/sql-client";

type ResultsTableProps = {
  errorMessage?: string;
  isProcessing: boolean;
  rows?: Array<Record<string, SqlScalar>>;
};

export function ResultsTable({
  errorMessage,
  isProcessing,
  rows = []
}: ResultsTableProps) {
  const columns = rows[0] ? Object.keys(rows[0]) : [];

  return (
    <Card className="overflow-hidden">
      <div className="flex items-center gap-3 border-b border-white/[0.08] p-5">
        <span className="grid size-10 place-items-center rounded-xl border border-emerald-400/20 bg-emerald-400/10 text-emerald-200">
          <Table2 className="size-5" />
        </span>
        <div>
          <h2 className="text-sm font-semibold text-white">Query Results</h2>
          <p className="text-xs text-slate-500">Mock output for the generated SQL.</p>
        </div>
      </div>

      {errorMessage ? (
        <StateMessage tone="error" message={errorMessage} />
      ) : isProcessing ? (
        <StateMessage message="Running generated SQL..." />
      ) : rows.length === 0 ? (
        <StateMessage message="Generate a query to see result rows." />
      ) : (
      <div className="overflow-x-auto">
        <table className="w-full min-w-[520px] text-left text-sm">
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
              <tr className="transition hover:bg-white/[0.03]" key={index}>
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
      )}
    </Card>
  );
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
