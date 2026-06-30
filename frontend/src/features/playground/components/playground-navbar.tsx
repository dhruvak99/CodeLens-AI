"use client";

import {
  ChevronDown,
  Moon,
  Play,
  Save,
  Settings,
  SlidersHorizontal
} from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";

type PlaygroundNavbarProps = {
  fileName: string;
  isRunning: boolean;
  onRun: () => void;
};

export function PlaygroundNavbar({
  fileName,
  isRunning,
  onRun
}: PlaygroundNavbarProps) {
  return (
    <header className="sticky top-0 z-40 border-b border-white/[0.08] bg-background/90 backdrop-blur-xl">
      <div className="flex h-16 items-center justify-between gap-3 px-4 lg:px-6">
        <Link className="flex items-center gap-3" href="/" aria-label="CodeLens AI home">
          <span className="grid size-9 place-items-center rounded-xl border border-primary/40 bg-primary/10 text-primary shadow-[0_0_30px_rgba(124,58,237,0.24)]">
            <SlidersHorizontal className="size-5" />
          </span>
          <span className="text-sm font-semibold tracking-tight text-white sm:text-lg">
            CodeLens <span className="text-primary">AI</span>
          </span>
        </Link>

        <div className="hidden min-w-0 flex-1 items-center justify-center md:flex">
          <button className="inline-flex max-w-[280px] items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.04] px-3 py-2 font-mono text-xs text-slate-200">
            <span className="size-2 rounded-full bg-amber-400" />
            <span className="truncate">{fileName}</span>
            <ChevronDown className="size-4 text-slate-500" />
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            className="grid size-10 place-items-center rounded-xl border border-white/[0.08] bg-white/[0.04] text-slate-300 transition hover:bg-white/[0.08]"
            aria-label="Theme toggle placeholder"
            type="button"
          >
            <Moon className="size-4" />
          </button>
          <button
            className="hidden h-10 items-center gap-2 rounded-xl border border-white/[0.08] bg-white/[0.04] px-3 text-sm text-slate-300 transition hover:bg-white/[0.08] sm:inline-flex"
            type="button"
          >
            <Save className="size-4" />
            Save
          </button>
          <Button onClick={onRun} size="sm" type="button">
            <Play className="size-4" />
            {isRunning ? "Running..." : "Run"}
          </Button>
          <button
            className="grid size-10 place-items-center rounded-xl border border-white/[0.08] bg-white/[0.04] text-slate-300 transition hover:bg-white/[0.08]"
            aria-label="Settings"
            type="button"
          >
            <Settings className="size-4" />
          </button>
        </div>
      </div>
      <div className="flex items-center justify-between border-t border-white/[0.06] px-4 py-2 md:hidden">
        <span className="truncate font-mono text-xs text-slate-300">{fileName}</span>
        <span className="text-xs text-emerald-300">Python</span>
      </div>
    </header>
  );
}
