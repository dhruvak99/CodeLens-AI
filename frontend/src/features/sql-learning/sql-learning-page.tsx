"use client";

import { useEffect, useMemo, useState } from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";

import { DatasetExplorer } from "@/features/sql-learning/components/dataset-explorer";
import { DatasetPreviewTable } from "@/features/sql-learning/components/dataset-preview-table";
import { ExplanationCard } from "@/features/sql-learning/components/explanation-card";
import { GeneratedSqlCard } from "@/features/sql-learning/components/generated-sql-card";
import { NaturalLanguageQueryCard } from "@/features/sql-learning/components/nl-query-card";
import { ResultsTable } from "@/features/sql-learning/components/results-table";
import { SchemaCard } from "@/features/sql-learning/components/schema-card";
import {
  getSqlSchema,
  getSqlTablePreview,
  getSqlTables,
  processSqlQuery,
  type SqlQueryProcessResponse
} from "@/lib/api/sql-client";

export function SqlLearningPage() {
  const [tableName, setTableName] = useState("");
  const [query, setQuery] = useState("");
  const [queryResult, setQueryResult] = useState<SqlQueryProcessResponse | null>(null);

  const tablesQuery = useQuery({
    queryKey: ["sql", "tables"],
    queryFn: ({ signal }) => getSqlTables(signal)
  });

  const schemaQuery = useQuery({
    queryKey: ["sql", "schema"],
    queryFn: ({ signal }) => getSqlSchema(signal)
  });

  const tables = useMemo(() => tablesQuery.data?.tables ?? [], [tablesQuery.data?.tables]);

  useEffect(() => {
    if (!tableName && tables[0]?.name) {
      setTableName(tables[0].name);
    }
  }, [tableName, tables]);

  const previewQuery = useQuery({
    enabled: tableName.length > 0,
    queryKey: ["sql", "table-preview", tableName],
    queryFn: ({ signal }) => getSqlTablePreview(tableName, signal)
  });

  const schemaTable = useMemo(
    () => schemaQuery.data?.tables.find((table) => table.name === tableName),
    [schemaQuery.data?.tables, tableName]
  );

  const queryMutation = useMutation({
    mutationFn: processSqlQuery,
    onSuccess: (response) => {
      setQueryResult(response);
    }
  });

  const handleGenerateSql = () => {
    const trimmedQuery = query.trim();

    if (!trimmedQuery || queryMutation.isPending) {
      return;
    }

    setQueryResult(null);
    queryMutation.mutate({
      query: trimmedQuery,
      selected_table: tableName,
      mode: "learning"
    });
  };

  const queryErrorMessage = queryMutation.isError
    ? "Unable to process the SQL request. Check that the SemanticSQL backend is running."
    : undefined;

  return (
    <motion.div
      animate={{ opacity: 1, y: 0 }}
      className="mx-auto flex max-w-[1440px] flex-col gap-4 p-3 sm:p-4 lg:p-6"
      initial={{ opacity: 0, y: 16 }}
      transition={{ duration: 0.35, ease: "easeOut" }}
    >
      <section className="rounded-2xl border border-white/[0.08] bg-white/[0.03] p-5 sm:p-6">
        <p className="mb-3 font-mono text-xs uppercase tracking-[0.28em] text-cyan-300">
          SQL Lab
        </p>
        <h1 className="text-2xl font-semibold tracking-tight text-white sm:text-3xl">
          Database Query Lab
        </h1>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400 sm:text-base">
          Practice SQL by converting natural language into SQL queries and
          understand how the query works.
        </p>
      </section>

      <section className="grid gap-4 lg:grid-cols-[0.8fr_1.2fr]">
        <DatasetExplorer
          columnCount={schemaTable?.columns.length}
          errorMessage={
            tablesQuery.isError
              ? "Unable to load tables. Check that the SemanticSQL backend is running on port 8001."
              : undefined
          }
          isLoading={tablesQuery.isLoading}
          onTableChange={setTableName}
          selectedTableName={tableName}
          tables={tables}
        />
        <NaturalLanguageQueryCard
          isProcessing={queryMutation.isPending}
          onGenerate={handleGenerateSql}
          onQueryChange={setQuery}
          query={query}
        />
      </section>

      <DatasetPreviewTable
        errorMessage={
          previewQuery.isError
            ? "Unable to load table preview for the selected table."
            : undefined
        }
        isLoading={previewQuery.isFetching}
        preview={previewQuery.data}
        tableName={tableName}
      />
      <GeneratedSqlCard sql={queryResult?.generated_sql} />
      <ResultsTable
        errorMessage={queryErrorMessage}
        isProcessing={queryMutation.isPending}
        rows={queryResult?.results}
      />

      <section className="grid gap-4 lg:grid-cols-2">
        <SchemaCard
          errorMessage={
            schemaQuery.isError
              ? "Unable to load schema information from SemanticSQL."
              : undefined
          }
          isLoading={schemaQuery.isLoading}
          schemaTable={schemaTable}
          tableName={tableName}
        />
        <ExplanationCard explanation={queryResult?.explanation ?? buildExplanation(queryResult)} />
      </section>
    </motion.div>
  );
}

function buildExplanation(response: SqlQueryProcessResponse | null) {
  if (!response) {
    return undefined;
  }

  if (response.explanation?.trim()) {
    return response.explanation;
  }

  if (response.validation_errors.length > 0) {
    return `SemanticSQL generated SQL, but validation reported: ${response.validation_errors.join(
      ", "
    )}`;
  }

  return `SemanticSQL generated a ${response.generation_mode} query that returned ${response.rows_returned} row${
    response.rows_returned === 1 ? "" : "s"
  } in ${response.execution_time.toFixed(3)} seconds. Validation status: ${
    response.validation_status
  }.`;
}
