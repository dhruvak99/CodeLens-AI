import { Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";

type ExplanationCardProps = {
  explanation?: string;
};

export function ExplanationCard({ explanation }: ExplanationCardProps) {
  const blocks = parseMarkdown(explanation?.trim() ?? "");

  return (
    <Card className="p-5">
      <div className="mb-5 flex items-center gap-3">
        <span className="grid size-10 place-items-center rounded-xl border border-primary/30 bg-primary/10 text-primary">
          <Sparkles className="size-5" />
        </span>
        <div>
          <h2 className="text-sm font-semibold text-white">AI Explanation</h2>
          <p className="text-xs text-slate-500">SemanticSQL response summary.</p>
        </div>
      </div>

      <div className="rounded-xl border border-white/[0.06] bg-slate-950/50 p-4 text-sm leading-7 text-slate-300">
        {blocks.length > 0 ? (
          <div className="space-y-4">{blocks.map(renderBlock)}</div>
        ) : (
          "Generate a query to see the backend explanation here."
        )}
      </div>
    </Card>
  );
}

type MarkdownBlock =
  | { type: "heading"; text: string }
  | { type: "paragraph"; text: string }
  | { type: "list"; items: string[] }
  | { type: "code"; code: string };

function parseMarkdown(markdown: string): MarkdownBlock[] {
  const blocks: MarkdownBlock[] = [];
  const lines = markdown.split("\n");
  let paragraph: string[] = [];
  let listItems: string[] = [];
  let codeLines: string[] = [];
  let inCode = false;

  const flushParagraph = () => {
    if (paragraph.length > 0) {
      blocks.push({ type: "paragraph", text: paragraph.join(" ") });
      paragraph = [];
    }
  };
  const flushList = () => {
    if (listItems.length > 0) {
      blocks.push({ type: "list", items: listItems });
      listItems = [];
    }
  };

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith("```")) {
      if (inCode) {
        blocks.push({ type: "code", code: codeLines.join("\n") });
        codeLines = [];
        inCode = false;
      } else {
        flushParagraph();
        flushList();
        inCode = true;
      }
      continue;
    }
    if (inCode) {
      codeLines.push(line);
      continue;
    }
    if (!trimmed) {
      flushParagraph();
      flushList();
      continue;
    }
    if (trimmed.startsWith("## ")) {
      flushParagraph();
      flushList();
      blocks.push({ type: "heading", text: trimmed.replace(/^##\s+/, "") });
      continue;
    }
    if (trimmed.startsWith("- ")) {
      flushParagraph();
      listItems.push(trimmed.replace(/^-\s+/, ""));
      continue;
    }
    flushList();
    paragraph.push(trimmed);
  }

  flushParagraph();
  flushList();
  if (codeLines.length > 0) {
    blocks.push({ type: "code", code: codeLines.join("\n") });
  }
  return blocks;
}

function renderBlock(block: MarkdownBlock, index: number) {
  if (block.type === "heading") {
    return (
      <h3 className="text-sm font-semibold text-white" key={index}>
        {block.text}
      </h3>
    );
  }
  if (block.type === "list") {
    return (
      <ul className="list-disc space-y-1 pl-5" key={index}>
        {block.items.map((item) => (
          <li key={item}>{renderInlineCode(item)}</li>
        ))}
      </ul>
    );
  }
  if (block.type === "code") {
    return (
      <pre
        className="overflow-x-auto rounded-lg border border-white/[0.08] bg-slate-950 p-3 font-mono text-xs leading-6 text-cyan-100"
        key={index}
      >
        <code>{block.code}</code>
      </pre>
    );
  }
  return <p key={index}>{renderInlineCode(block.text)}</p>;
}

function renderInlineCode(text: string) {
  const parts = text.split(/(`[^`]+`)/g);
  return parts.map((part, index) =>
    part.startsWith("`") && part.endsWith("`") ? (
      <code
        className="rounded border border-white/[0.08] bg-white/[0.05] px-1 py-0.5 font-mono text-xs text-cyan-100"
        key={index}
      >
        {part.slice(1, -1)}
      </code>
    ) : (
      <span key={index}>{part}</span>
    )
  );
}
