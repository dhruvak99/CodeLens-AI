"use client";

import type { ReactNode } from "react";
import { ChevronDown, Database } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { SqlTableSummary } from "@/lib/api/sql-client";

type DatasetExplorerProps = {
  columnCount?: number;
  errorMessage?: string;
  isLoading: boolean;
  onTableChange: (tableName: string) => void;
  selectedTableName: string;
  tables: SqlTableSummary[];
};

export function DatasetExplorer({
  columnCount: schemaColumnCount,
  errorMessage,
  isLoading,
  onTableChange,
  selectedTableName,
  tables
}: DatasetExplorerProps) {
  const selectedTable = tables.find((table) => table.name === selectedTableName);
  const rowCount = selectedTable?.row_count ?? selectedTable?.rowCount;
  const columnCount =
    schemaColumnCount ?? selectedTable?.column_count ?? selectedTable?.columnCount;

  return (
    <Card className="p-5">
      <div className="mb-5 flex items-center gap-3">
        <span className="grid size-10 place-items-center rounded-xl border border-cyan-400/20 bg-cyan-400/10 text-cyan-200">
          <Database className="size-5" />
        </span>
        <div>
          <h2 className="text-sm font-semibold text-white">Dataset Explorer</h2>
          <p className="text-xs text-slate-500">Browse live SQL datasets.</p>
        </div>
      </div>

      {errorMessage ? (
        <div className="rounded-xl border border-red-400/20 bg-red-500/10 p-4 text-sm text-red-100">
          {errorMessage}
        </div>
      ) : (
        <div>
          <label
            className="mb-2 block text-xs font-medium text-slate-400"
            htmlFor="sql-table"
          >
            Table
          </label>
          <SelectShell>
            <select
              className="h-11 w-full appearance-none bg-transparent px-3 pr-10 text-sm text-slate-100 outline-none"
              id="sql-table"
              disabled={isLoading || tables.length === 0}
              onChange={(event) => onTableChange(event.target.value)}
              value={selectedTableName}
            >
              {tables.map((table) => (
                <option
                  className="bg-slate-950 text-slate-100"
                  key={table.name}
                  value={table.name}
                >
                  {table.name}
                </option>
              ))}
            </select>
          </SelectShell>
        </div>
      )}

      <div className="mt-5 grid grid-cols-2 gap-3">
        <Stat label="Rows" value={isLoading ? "Loading" : rowCount ?? "—"} />
        <Stat label="Columns" value={isLoading ? "Loading" : columnCount ?? "—"} />
      </div>
    </Card>
  );
}

function SelectShell({ children }: { children: ReactNode }) {
  return (
    <div className="relative rounded-xl border border-white/[0.08] bg-white/[0.04] transition hover:border-white/[0.14] focus-within:border-primary/60">
      {children}
      <ChevronDown className="pointer-events-none absolute right-3 top-1/2 size-4 -translate-y-1/2 text-slate-500" />
    </div>
  );
}

function Stat({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded-xl border border-white/[0.06] bg-slate-950/40 p-4">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 font-mono text-xl font-semibold text-white">{value}</p>
    </div>
  );
}
