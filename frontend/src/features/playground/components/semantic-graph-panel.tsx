"use client";

import { useMemo } from "react";
import ReactFlow, { Background, Controls, type Edge, type Node } from "reactflow";

import { PanelShell } from "@/features/playground/components/panel-shell";
import type { SemanticGraph } from "@/lib/api/contracts";

type SemanticGraphPanelProps = {
  graph: SemanticGraph;
  isAnalyzing: boolean;
};

const nodeClassByType: Record<string, string> = {
  class: "semantic-node class-node",
  conditional: "semantic-node conditional-node",
  function: "semantic-node function-node",
  loop: "semantic-node loop-node",
  variable: "semantic-node variable-node"
};

function graphNodePosition(index: number) {
  const column = index % 3;
  const row = Math.floor(index / 3);

  return {
    x: 40 + column * 190,
    y: 36 + row * 118
  };
}

export function SemanticGraphPanel({
  graph,
  isAnalyzing
}: SemanticGraphPanelProps) {
  const shouldHideLonelyGlobalNode =
    graph.nodes.length === 1 &&
    graph.nodes[0]?.label.toLowerCase() === "global" &&
    graph.edges.length === 0;
  const graphForDisplay = shouldHideLonelyGlobalNode
    ? { nodes: [], edges: [] }
    : graph;
  const nodes = useMemo<Node[]>(
    () =>
      graphForDisplay.nodes.map((node, index) => ({
        id: node.id,
        data: { label: node.label },
        position: graphNodePosition(index),
        type: "default",
        className: nodeClassByType[node.type] ?? "semantic-node"
      })),
    [graphForDisplay.nodes]
  );

  const edges = useMemo<Edge[]>(
    () =>
      graphForDisplay.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
        label: edge.label,
        animated: edge.label === "modifies" || edge.label === "depends_on",
        style: {
          stroke: edge.label === "modifies" ? "#06B6D4" : "#7C3AED"
        }
      })),
    [graphForDisplay.edges]
  );

  return (
    <PanelShell
      title="Semantic Graph"
      eyebrow="Function · Variable · Loop"
      className="h-[360px] min-h-[300px] max-h-[560px] resize-y"
      bodyClassName="relative"
    >
      {isAnalyzing ? (
        <div className="absolute left-3 top-3 z-10 rounded-full border border-primary/30 bg-primary/15 px-3 py-1.5 text-xs text-primary">
          Analyzing...
        </div>
      ) : null}
      {nodes.length === 0 ? (
        <div className="grid h-full place-items-center p-6 text-center">
          <div className="rounded-xl border border-dashed border-white/[0.12] px-6 py-8">
            <p className="text-sm font-medium text-white">
              No semantic graph available.
            </p>
            <p className="mt-1 text-xs text-slate-500">
              Start typing to generate a graph.
            </p>
          </div>
        </div>
      ) : (
        <ReactFlow
          edges={edges}
          fitView
          fitViewOptions={{ padding: 0.28 }}
          nodes={nodes}
          nodesDraggable
          panOnScroll
        >
          <Background color="rgba(255,255,255,0.08)" gap={18} />
          <Controls position="top-right" showInteractive={false} />
        </ReactFlow>
      )}
      <div className="pointer-events-none absolute bottom-3 left-3 flex flex-wrap gap-2 text-[10px] text-slate-400">
        <span className="rounded-full border border-white/[0.08] bg-background/80 px-2 py-1">
          modifies
        </span>
        <span className="rounded-full border border-white/[0.08] bg-background/80 px-2 py-1">
          depends_on
        </span>
      </div>
    </PanelShell>
  );
}
