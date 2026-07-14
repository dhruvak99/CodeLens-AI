import type { ReactNode } from "react";
import { Braces } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { SqlSchemaTable } from "@/lib/api/sql-client";

type SchemaCardProps = {
  errorMessage?: string;
  isLoading: boolean;
  schemaTable?: SqlSchemaTable;
  tableName: string;
};

export function SchemaCard({
  errorMessage,
  isLoading,
  schemaTable,
  tableName
}: SchemaCardProps) {
  return (
    <Card className="p-5">
      <div className="mb-5 flex items-center gap-3">
        <span className="grid size-10 place-items-center rounded-xl border border-amber-300/20 bg-amber-300/10 text-amber-200">
          <Braces className="size-5" />
        </span>
        <div>
          <h2 className="text-sm font-semibold text-white">Schema Information</h2>
          <p className="text-xs text-slate-500">{tableName || "Selected table"}</p>
        </div>
      </div>

      {errorMessage ? (
        <StateMessage tone="error" message={errorMessage} />
      ) : isLoading ? (
        <StateMessage message="Loading schema..." />
      ) : !schemaTable ? (
        <StateMessage message="No schema information available for this table." />
      ) : (
        <div className="space-y-2">
          {schemaTable.columns.map((column) => (
            <div
              className="flex flex-wrap items-center gap-2 rounded-xl border border-white/[0.06] bg-white/[0.03] px-3 py-3"
              key={column.name}
            >
              <span className="mr-auto font-mono text-xs font-semibold text-cyan-200">
                {column.name}
              </span>
              <span className="font-mono text-xs text-slate-500">
                {column.type}
              </span>
              {column.primary_key === true ? <Badge>Primary Key</Badge> : null}
              {column.not_null === true || column.nullable === false ? (
                <Badge>Not Null</Badge>
              ) : null}
              {column.nullable === true ? (
                <Badge tone="neutral">Nullable</Badge>
              ) : null}
            </div>
          ))}
        </div>
      )}
    </Card>
  );
}

function Badge({
  children,
  tone = "primary"
}: {
  children: ReactNode;
  tone?: "primary" | "neutral";
}) {
  return (
    <span
      className={`w-fit rounded-full border px-2 py-1 text-[10px] font-medium ${
        tone === "primary"
          ? "border-primary/30 bg-primary/10 text-primary"
          : "border-white/[0.08] bg-white/[0.04] text-slate-400"
      }`}
    >
      {children}
    </span>
  );
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
      className={`rounded-xl border p-4 text-sm ${
        tone === "error"
          ? "border-red-400/20 bg-red-500/10 text-red-100"
          : "border-white/[0.06] bg-slate-950/40 text-slate-400"
      }`}
    >
      {message}
    </div>
  );
}
