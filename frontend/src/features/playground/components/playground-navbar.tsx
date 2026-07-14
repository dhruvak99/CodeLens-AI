"use client";

import { useEffect, useState } from "react";
import {
  Moon,
  SlidersHorizontal,
  Sun
} from "lucide-react";
import Link from "next/link";

import {
  WorkspaceSelector,
  type WorkspaceId
} from "@/features/sql-learning/components/workspace-selector";

type PlaygroundNavbarProps = {
  activeWorkspace: WorkspaceId;
  onWorkspaceChange: (workspace: WorkspaceId) => void;
};

type ThemeMode = "dark" | "light";

export function PlaygroundNavbar({
  activeWorkspace,
  onWorkspaceChange
}: PlaygroundNavbarProps) {
  const [theme, setTheme] = useState<ThemeMode>("dark");

  useEffect(() => {
    const savedTheme = window.localStorage.getItem("codelens-theme");
    const initialTheme: ThemeMode = savedTheme === "light" ? "light" : "dark";

    setTheme(initialTheme);
    document.documentElement.classList.toggle("light", initialTheme === "light");
    document.documentElement.classList.toggle("dark", initialTheme === "dark");
    document.documentElement.style.colorScheme = initialTheme;
  }, []);

  const toggleTheme = () => {
    const nextTheme: ThemeMode = theme === "dark" ? "light" : "dark";

    setTheme(nextTheme);
    window.localStorage.setItem("codelens-theme", nextTheme);
    document.documentElement.classList.toggle("light", nextTheme === "light");
    document.documentElement.classList.toggle("dark", nextTheme === "dark");
    document.documentElement.style.colorScheme = nextTheme;
  };

  const ThemeIcon = theme === "dark" ? Moon : Sun;

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
          <WorkspaceSelector
            activeWorkspace={activeWorkspace}
            className="max-w-[320px]"
            onWorkspaceChange={onWorkspaceChange}
          />
        </div>

        <div className="flex items-center gap-2">
          <button
            className="grid size-10 place-items-center rounded-xl border border-white/[0.08] bg-white/[0.04] text-slate-300 transition hover:bg-white/[0.08]"
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} theme`}
            onClick={toggleTheme}
            title={`Switch to ${theme === "dark" ? "light" : "dark"} theme`}
            type="button"
          >
            <ThemeIcon className="size-4" />
          </button>
        </div>
      </div>
      <div className="flex items-center justify-between border-t border-white/[0.06] px-4 py-2 md:hidden">
        <WorkspaceSelector
          activeWorkspace={activeWorkspace}
          className="w-full justify-between"
          onWorkspaceChange={onWorkspaceChange}
        />
      </div>
    </header>
  );
}
