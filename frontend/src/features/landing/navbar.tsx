import { ArrowRight, Github } from "lucide-react";
import Link from "next/link";

import { Button } from "@/components/ui/button";
import { logoIcon as LogoIcon, navItems } from "@/features/landing/data";
import { MotionHeader } from "@/features/landing/motion";

export function Navbar() {
  return (
    <MotionHeader
      animate={{ y: 0, opacity: 1 }}
      className="fixed inset-x-0 top-0 z-50 border-b border-white/[0.08] bg-background/78 backdrop-blur-xl"
      initial={{ y: -16, opacity: 0 }}
      transition={{ duration: 0.45, ease: "easeOut" }}
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <a className="flex items-center gap-3" href="#top" aria-label="CodeLens AI">
          <span className="grid size-9 place-items-center rounded-xl border border-primary/40 bg-primary/10 text-primary shadow-[0_0_30px_rgba(124,58,237,0.28)]">
            <LogoIcon className="size-5" />
          </span>
          <span className="text-base font-semibold tracking-tight sm:text-lg">
            CodeLens <span className="text-primary">AI</span>
          </span>
        </a>

        <nav className="hidden items-center gap-1 md:flex" aria-label="Main">
          {navItems.map((item) => (
            <a
              className="rounded-lg px-3 py-2 text-sm text-slate-300 transition hover:bg-white/[0.05] hover:text-white"
              href={item.href}
              key={item.label}
            >
              {item.label === "GitHub" ? (
                <span className="inline-flex items-center gap-2">
                  <Github className="size-4" />
                  {item.label}
                </span>
              ) : (
                item.label
              )}
            </a>
          ))}
        </nav>

        <Button asChild size="sm">
          <Link href="/playground">
            Open Playground
            <ArrowRight className="size-4" />
          </Link>
        </Button>
      </div>
      <nav
        aria-label="Mobile main"
        className="mx-auto flex max-w-7xl gap-2 overflow-x-auto border-t border-white/[0.06] px-4 py-2 md:hidden"
      >
        {navItems.map((item) => (
          <a
            className="shrink-0 rounded-lg border border-white/[0.08] bg-white/[0.03] px-3 py-1.5 text-xs text-slate-300"
            href={item.href}
            key={item.label}
          >
            {item.label}
          </a>
        ))}
      </nav>
    </MotionHeader>
  );
}
