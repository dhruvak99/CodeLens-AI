import { footerLinks } from "@/features/landing/data";

export function Footer() {
  return (
    <footer
      className="border-t border-white/[0.08] px-4 py-8 sm:px-6 lg:px-8"
      id="version"
    >
      <div className="mx-auto flex max-w-7xl flex-col gap-5 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between">
        <p>© 2026 CodeLens AI. All rights reserved.</p>
        <div className="flex flex-wrap items-center gap-4">
          {footerLinks.map((link) => (
            <a
              className="transition hover:text-white"
              href={link.href}
              key={link.label}
            >
              {link.label}
            </a>
          ))}
          <span className="font-mono text-xs text-slate-600">v0.1.0</span>
        </div>
      </div>
    </footer>
  );
}
