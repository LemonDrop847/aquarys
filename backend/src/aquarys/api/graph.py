"""API router for relational Evidence Graph endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from aquarys.core.database import get_db
from aquarys.schemas.graph import EvidenceGraphResponse
from aquarys.services.graph.builder import build_evidence_graph_for_site

router = APIRouter(prefix="/evidence", tags=["Evidence Graph"])


@router.get("/graph/{site_id}", response_model=EvidenceGraphResponse)
async def get_site_evidence_graph(
    site_id: str,
    persist: bool = False,
    db: AsyncSession = Depends(get_db),
) -> EvidenceGraphResponse:
    """Retrieve or construct the relational Evidence Graph for a site."""
    graph = await build_evidence_graph_for_site(db, site_id, persist=persist)
    nodes = graph["nodes"]
    edges = graph["edges"]
    if not nodes:
        raise HTTPException(status_code=404, detail=f"No telemetry found for site {site_id}")

    contradictions = [e for e in edges if e.edge_type == "contradicts"]
    supports = [e for e in edges if e.edge_type == "supports"]

    return EvidenceGraphResponse(
        site_id=site_id,
        node_count=len(nodes),
        edge_count=len(edges),
        contradiction_count=len(contradictions),
        support_count=len(supports),
        nodes=[
            {
                "id": n.id,
                "node_type": n.node_type,
                "label": n.label,
                "description": n.description,
                "confidence": n.confidence,
                "source_reference": n.source_reference,
                "properties": n.properties,
                "created_at": n.created_at,
            }
            for n in nodes
        ],
        edges=[
            {
                "id": e.id,
                "source_node_id": e.source_node_id,
                "target_node_id": e.target_node_id,
                "edge_type": e.edge_type,
                "weight": e.weight,
                "reason": e.reason,
                "created_at": e.created_at,
            }
            for e in edges
        ],
    )
