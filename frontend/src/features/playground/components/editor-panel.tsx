"use client";

import { useEffect, useRef } from "react";
import Editor, { type BeforeMount, type OnMount } from "@monaco-editor/react";
import { Loader2 } from "lucide-react";

import { PanelShell } from "@/features/playground/components/panel-shell";

type EditorPanelProps = {
  code: string;
  onCodeChange: (value: string) => void;
  isAnalyzing: boolean;
  focusTarget: {
    line: number;
    nonce: number;
  } | null;
};

const configureMonaco: BeforeMount = (monaco) => {
  monaco.editor.defineTheme("codelens-dark", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "keyword", foreground: "C084FC" },
      { token: "number", foreground: "FBBF24" },
      { token: "string", foreground: "86EFAC" },
      { token: "comment", foreground: "64748B" }
    ],
    colors: {
      "editor.background": "#050B18",
      "editorLineNumber.foreground": "#64748B",
      "editorCursor.foreground": "#7C3AED",
      "editor.lineHighlightBackground": "#111827",
      "editor.selectionBackground": "#7C3AED55"
    }
  });
};

export function EditorPanel({
  code,
  onCodeChange,
  isAnalyzing,
  focusTarget
}: EditorPanelProps) {
  const editorRef = useRef<Parameters<OnMount>[0] | null>(null);
  const monacoRef = useRef<Parameters<OnMount>[1] | null>(null);
  const decorationsRef = useRef<string[]>([]);

  const handleMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
  };

  useEffect(() => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;

    if (!editor || !monaco || !focusTarget) {
      return;
    }

    const line = Math.max(1, focusTarget.line);

    editor.focus();
    editor.revealLineInCenter(line, monaco.editor.ScrollType.Smooth);
    editor.setPosition({ lineNumber: line, column: 1 });
    decorationsRef.current = editor.deltaDecorations(decorationsRef.current, [
      {
        range: new monaco.Range(line, 1, line, 1),
        options: {
          isWholeLine: true,
          className: "codelens-line-highlight",
          overviewRuler: {
            color: "#7C3AED",
            position: monaco.editor.OverviewRulerLane.Center
          }
        }
      }
    ]);
  }, [focusTarget]);

  return (
    <PanelShell
      title="binary_search.py"
      eyebrow="Python · Monaco Editor"
      className="h-[520px] min-h-[420px] max-h-[760px] resize-y lg:resize-x"
      actions={
        <span className="rounded-lg border border-white/[0.08] bg-white/[0.04] px-2 py-1 text-xs text-slate-400">
          UTF-8
        </span>
      }
      bodyClassName="relative"
    >
      {isAnalyzing ? (
        <div className="absolute right-4 top-4 z-10 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/15 px-3 py-1.5 text-xs text-primary">
          <Loader2 className="size-3.5 animate-spin" />
          Analyzing...
        </div>
      ) : null}
      <Editor
        beforeMount={configureMonaco}
        defaultLanguage="python"
        loading={
          <div className="flex h-full items-center justify-center gap-2 text-sm text-slate-400">
            <Loader2 className="size-4 animate-spin" />
            Loading editor
          </div>
        }
        onMount={handleMount}
        onChange={(value) => onCodeChange(value ?? "")}
        options={{
          minimap: { enabled: false },
          fontFamily: "var(--font-jetbrains-mono)",
          fontSize: 14,
          lineHeight: 24,
          padding: { top: 18, bottom: 18 },
          scrollBeyondLastLine: false,
          smoothScrolling: true,
          cursorBlinking: "smooth",
          renderLineHighlight: "all",
          overviewRulerBorder: false,
          wordWrap: "on"
        }}
        theme="codelens-dark"
        value={code}
        height="100%"
      />
      <div className="flex flex-wrap items-center justify-between gap-2 border-t border-white/[0.08] px-4 py-3 text-xs text-slate-500">
        <span className="text-emerald-300">Ready</span>
        <span>Ln 9, Col 20</span>
        <span>Spaces: 4</span>
        <span>Python 3.12</span>
      </div>
    </PanelShell>
  );
}
