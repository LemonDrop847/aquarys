"use client";

import { useCallback, useState } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Node,
  Edge,
  ConnectionLineType,
  MarkerType,
  useNodesState,
  useEdgesState
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { EvidenceGraph, EvidenceNode } from "@/lib/types";
import { CustomEvidenceNode } from "./CustomEvidenceNode";
import { NodeInspector } from "./NodeInspector";

const EDGE_COLORS = {
  supports: "#34d399",
  contradicts: "#f87171",
  derived_from: "#60a5fa",
  correlates: "#a78bfa",
  located_at: "#fbbf24"
};

type EvidenceNodeData = EvidenceNode & Record<string, unknown>;

interface EvidenceGraphViewProps {
  graph: EvidenceGraph;
}

export function EvidenceGraphView({ graph }: EvidenceGraphViewProps) {
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  const initialNodes: Node<EvidenceNodeData>[] = graph.nodes.map((node, idx) => ({
    id: node.id,
    type: "evidenceNode",
    position: { x: (idx % 3) * 320, y: Math.floor(idx / 3) * 180 },
    data: { ...node } as EvidenceNodeData
  }));

  const initialEdges: Edge[] = graph.edges.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    type: ConnectionLineType.SmoothStep,
    animated: edge.type === "supports" || edge.type === "contradicts",
    style: {
      stroke: EDGE_COLORS[edge.type] || "#64748b",
      strokeWidth: Math.max(1, edge.strength / 33)
    },
    markerEnd: {
      type: MarkerType.ArrowClosed,
      color: EDGE_COLORS[edge.type] || "#64748b"
    },
    label: edge.type.replace("_", " "),
    labelStyle: {
      fontSize: "10px",
      fontFamily: "monospace",
      fill: "#94a3b8",
      fontWeight: "bold"
    },
    labelBgStyle: {
      fill: "#020617",
      fillOpacity: 0.9
    }
  }));

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onNodeClick = useCallback((_: React.MouseEvent, node: Node) => {
    setSelectedNodeId(node.id);
  }, []);

  const handleCloseInspector = useCallback(() => {
    setSelectedNodeId(null);
  }, []);

  const selectedNode = selectedNodeId
    ? graph.nodes.find((n) => n.id === selectedNodeId) || null
    : null;

  return (
    <div className="relative w-full h-[600px] rounded-xl bg-slate-950/90 border border-slate-800 overflow-hidden font-mono">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        nodeTypes={{ evidenceNode: CustomEvidenceNode }}
        connectionLineType={ConnectionLineType.SmoothStep}
        fitView
        minZoom={0.2}
        maxZoom={1.5}
        className="bg-slate-950"
      >
        <Background color="#1e293b" gap={16} />
        <Controls className="bg-slate-900 border-slate-700 text-slate-300" />
        <MiniMap
          nodeColor={(node) => {
            const type = (node.data as EvidenceNodeData)?.type;
            const colors: Record<string, string> = {
              claim: "#22d3ee",
              observation: "#34d399",
              measurement: "#60a5fa",
              eo_signal: "#a78bfa",
              site: "#fbbf24",
              hypothesis: "#fb7185",
              intervention: "#818cf8"
            };
            return (type && colors[type]) || "#64748b";
          }}
          className="bg-slate-900/90 border-slate-700"
        />
      </ReactFlow>

      <NodeInspector node={selectedNode} onClose={handleCloseInspector} />
    </div>
  );
}
