import {
  CheckCircle2,
  ChevronRight,
  Database,
  Play,
  Sparkles
} from "lucide-react";
import type { ReactNode } from "react";

import { Card } from "@/components/ui/card";
import { codeLines, findings } from "@/features/landing/data";
import { cn } from "@/lib/utils";

const toneStyles = {
  red: "border-red-400/40 bg-red-500/10 text-red-200",
  amber: "border-amber-400/40 bg-amber-500/10 text-amber-200",
  blue: "border-sky-400/40 bg-sky-500/10 text-sky-200"
};

export function PythonShowcase() {
  return (
    <Card
      className="relative overflow-hidden rounded-[1.35rem] bg-[#050B18]/95"
      id="playground-preview"
    >
      <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3">
        <div>
          <p className="text-sm font-semibold text-white">Python Lab</p>
          <p className="font-mono text-xs text-slate-500">binary_search.py</p>
        </div>
        <button className="inline-flex items-center gap-1 rounded-lg bg-primary px-3 py-1.5 text-xs text-white shadow-[0_0_22px_rgba(124,58,237,0.35)]">
          <Play className="size-3" />
          Run Analysis
        </button>
      </div>

      <div className="grid border-b border-white/[0.08] xl:grid-cols-[1fr_240px]">
        <div className="grid min-h-[320px] grid-cols-[40px_1fr] overflow-hidden font-mono text-[11px] leading-6">
          <div className="border-r border-white/[0.06] bg-white/[0.02] py-4 text-right text-slate-600">
            {codeLines.map((_, index) => (
              <div className="pr-3" key={index}>
                {index + 1}
              </div>
            ))}
          </div>
          <pre className="overflow-x-auto py-4 text-slate-300">
            {codeLines.map((line, index) => (
              <code
                className={cn(
                  "block px-4",
                  index === 8 &&
                    "border-y border-primary/15 bg-primary/10 text-white"
                )}
                key={`${line}-${index}`}
              >
                <span className="text-slate-500">{line.slice(0, 4)}</span>
                {line.slice(4)}
              </code>
            ))}
          </pre>
        </div>

        <aside className="border-t border-white/[0.08] bg-white/[0.02] p-4 xl:border-l xl:border-t-0">
          <div className="mb-4 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-white">Findings</h3>
            <span className="rounded-md bg-primary/20 px-2 py-1 text-xs text-primary">
              3
            </span>
          </div>
          <div className="space-y-3">
            {findings.slice(0, 2).map((finding) => (
              <div
                className="rounded-xl border border-white/[0.08] bg-[#0B1222] p-3"
                key={finding.title}
              >
                <div className="mb-2 flex items-center justify-between gap-3">
                  <p className="text-xs font-medium text-white">
                    {finding.title}
                  </p>
                  <span
                    className={cn(
                      "rounded-full border px-2 py-0.5 text-[10px]",
                      toneStyles[finding.tone as keyof typeof toneStyles]
                    )}
                  >
                    {finding.severity}
                  </span>
                </div>
                <p className="text-xs leading-5 text-slate-400">
                  {finding.detail}
                </p>
              </div>
            ))}
          </div>
        </aside>
      </div>

      <div className="grid border-b border-white/[0.08] sm:grid-cols-2">
        <PythonPanel title="Runtime Trace">
          <div className="space-y-2 font-mono text-[10px] text-slate-500">
            <p>step 04 · mid = 4 · arr[mid] = 9</p>
            <p className="text-red-300">step 05 · high = mid - 1</p>
          </div>
        </PythonPanel>
        <PythonPanel title="Metrics">
          <div className="grid grid-cols-2 gap-2 text-xs">
            <span className="text-slate-500">Time</span>
            <span className="text-emerald-300">O(log n)</span>
            <span className="text-slate-500">Cyclomatic</span>
            <span className="text-emerald-300">3</span>
          </div>
        </PythonPanel>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 text-xs text-slate-400">
        <span className="inline-flex items-center gap-2 text-emerald-300">
          <CheckCircle2 className="size-4" />
          Analysis completed
        </span>
        <span>Ln 9, Col 21</span>
        <span>32ms</span>
      </div>
    </Card>
  );
}

function PythonPanel({
  title,
  children
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="min-h-28 border-white/[0.08] p-4 sm:border-r sm:last:border-r-0">
      <div className="mb-3 flex items-center justify-between">
        <span className="text-xs font-medium text-white">{title}</span>
        <ChevronRight className="size-4 text-slate-600" />
      </div>
      {children}
    </div>
  );
}

export function SqlShowcase() {
  return (
    <Card className="relative overflow-hidden rounded-[1.35rem] bg-[#050B18]/95">
      <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3">
        <div>
          <p className="text-sm font-semibold text-white">SQL Lab</p>
          <p className="font-mono text-xs text-slate-500">students</p>
        </div>
        <span className="grid size-9 place-items-center rounded-xl border border-cyan-400/20 bg-cyan-400/10 text-cyan-200">
          <Database className="size-4" />
        </span>
      </div>

      <div className="grid gap-3 p-4">
        <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-4">
          <p className="text-xs font-semibold text-white">Dataset Explorer</p>
          <p className="mt-3 text-xs text-slate-500">Selected table</p>
          <p className="mt-1 font-mono text-sm text-cyan-200">students</p>
          <div className="mt-4 grid grid-cols-2 gap-2">
            <Metric label="Rows" value="240" />
            <Metric label="Columns" value="5" />
          </div>
        </div>

        <FlowArrow />

        <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-4">
          <p className="text-xs font-semibold text-white">
            Natural Language Query
          </p>
          <p className="mt-3 rounded-lg border border-white/[0.08] bg-slate-950/60 p-3 text-sm text-slate-300">
            Show students with CGPA above 8
          </p>
        </div>

        <FlowArrow />

        <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-4">
          <p className="mb-3 text-xs font-semibold text-white">Generated SQL</p>
          <pre className="overflow-x-auto rounded-lg border border-white/[0.08] bg-slate-950/70 p-3 font-mono text-xs leading-6 text-cyan-100">
            <code>{`SELECT *
FROM students
WHERE cgpa > 8;`}</code>
          </pre>
        </div>

        <FlowArrow />

        <div className="overflow-hidden rounded-xl border border-white/[0.08] bg-white/[0.03]">
          <div className="border-b border-white/[0.08] px-4 py-3 text-xs font-semibold text-white">
            Query Results
          </div>
          <table className="w-full text-left text-xs">
            <thead className="bg-white/[0.03] text-slate-500">
              <tr>
                <th className="px-4 py-2 font-medium">student_id</th>
                <th className="px-4 py-2 font-medium">name</th>
                <th className="px-4 py-2 font-medium">cgpa</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-white/[0.06] text-slate-300">
              {[
                [1, "Rahul", 9.1],
                [4, "Sneha", 9.3],
                [6, "Pooja", 9.5],
                [9, "Divya", 9.7]
              ].map(([id, name, cgpa]) => (
                <tr key={id}>
                  <td className="px-4 py-2 font-mono text-slate-400">{id}</td>
                  <td className="px-4 py-2 text-white">{name}</td>
                  <td className="px-4 py-2 font-mono text-cyan-200">{cgpa}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <FlowArrow />

        <div className="rounded-xl border border-white/[0.08] bg-white/[0.03] p-4">
          <div className="mb-3 flex items-center gap-2">
            <Sparkles className="size-4 text-primary" />
            <p className="text-xs font-semibold text-white">AI SQL Tutor</p>
          </div>
          <p className="text-xs font-semibold text-slate-200">Summary</p>
          <p className="mt-2 text-sm leading-6 text-slate-400">
            This query filters students whose CGPA is greater than 8 using a
            WHERE clause.
          </p>
        </div>
      </div>
    </Card>
  );
}

function FlowArrow() {
  return (
    <div className="flex justify-center font-mono text-sm text-slate-600">
      ↓
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-white/[0.06] bg-slate-950/50 p-2">
      <p className="text-[10px] text-slate-500">{label}</p>
      <p className="mt-1 font-mono text-sm text-white">{value}</p>
    </div>
  );
}
