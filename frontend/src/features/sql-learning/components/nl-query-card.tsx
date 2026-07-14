"use client";

import { WandSparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

type NaturalLanguageQueryCardProps = {
  isProcessing: boolean;
  onGenerate: () => void;
  query: string;
  onQueryChange: (query: string) => void;
};

export function NaturalLanguageQueryCard({
  isProcessing,
  onGenerate,
  query,
  onQueryChange
}: NaturalLanguageQueryCardProps) {
  return (
    <Card className="p-5">
      <div className="mb-5 flex items-center justify-between gap-4">
        <div>
          <h2 className="text-sm font-semibold text-white">Natural Language Query</h2>
          <p className="text-xs text-slate-500">
            Describe the rows you want to retrieve.
          </p>
        </div>
      </div>

      <textarea
        className="min-h-32 w-full resize-none rounded-xl border border-white/[0.08] bg-slate-950/50 p-4 text-sm leading-6 text-slate-100 outline-none transition placeholder:text-slate-600 hover:border-white/[0.14] focus:border-primary/60"
        onChange={(event) => onQueryChange(event.target.value)}
        placeholder="Show employees earning more than 80000."
        value={query}
      />
      <Button
        className="mt-4"
        disabled={isProcessing || query.trim().length === 0}
        onClick={onGenerate}
        type="button"
      >
        <WandSparkles className="size-4" />
        {isProcessing ? "Generating..." : "Generate SQL"}
      </Button>
    </Card>
  );
}
