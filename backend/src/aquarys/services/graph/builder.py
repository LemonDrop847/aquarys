"""Evidence Graph builder: transforms multi-source telemetry into relational graph."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from aquarys.models import (
    EOMeasurement,
    EvidenceEdge,
    EvidenceNode,
    Measurement,
    Observation,
    Site,
)


def _utcnow() -> datetime:
    return datetime.now(UTC)


async def build_evidence_graph_for_site(
    db: AsyncSession,
    site_id: str,
    persist: bool = False,
) -> dict[str, Any]:
    """Constructs the Evidence Graph for a specific site from DB records."""

    # 1. Fetch site
    site_res = await db.execute(select(Site).where(Site.id == site_id))
    site = site_res.scalar_one_or_none()
    if not site:
        return {"nodes": [], "edges": []}

    # 2. Fetch observations with assessments
    obs_res = await db.execute(
        select(Observation)
        .where(Observation.site_id == site_id)
        .options(selectinload(Observation.assessment))
    )
    observations = list(obs_res.scalars().all())

    # 3. Fetch measurements
    meas_res = await db.execute(
        select(Measurement).where(Measurement.site_id == site_id)
    )
    measurements = list(meas_res.scalars().all())

    # 4. Fetch EO measurements
    eo_res = await db.execute(
        select(EOMeasurement).where(EOMeasurement.site_id == site_id)
    )
    eo_measurements = list(eo_res.scalars().all())

    nodes: list[EvidenceNode] = []
    edges: list[EvidenceEdge] = []

    # Central Site Node
    site_node_id = f"node:site:{site.id}"
    site_node = EvidenceNode(
        id=site_node_id,
        node_type="SITE",
        label=f"Site: {site.name} ({site.code})",
        description=f"Stream site in {site.city}, {site.country}",
        confidence=1.0,
        source_reference=f"sites/{site.id}",
        properties={
            "city": site.city,
            "country": site.country,
            "lat": site.latitude,
            "lon": site.longitude,
            "stream_name": site.stream_name,
        },
        created_at=_utcnow(),
    )
    nodes.append(site_node)

    # Observation Nodes & Edges
    obs_nodes_map: dict[str, EvidenceNode] = {}
    for obs in observations:
        obs_node_id = f"node:obs:{obs.id}"
        conf = obs.assessment.overall_confidence if obs.assessment else 0.8
        obs_node = EvidenceNode(
            id=obs_node_id,
            node_type="OBSERVATION",
            label=f"Observation {obs.id[:8]} ({obs.water_clarity or 'general'})",
            description=obs.notes or f"Citizen observation: clarity={obs.water_clarity}, flow={obs.flow_rate_category}, odor={obs.odor}",
            confidence=conf,
            source_reference=f"observations/{obs.id}",
            properties={
                "observed_at": obs.observed_at.isoformat() if obs.observed_at else None,
                "observer_type": obs.observer_type,
                "water_clarity": obs.water_clarity,
                "flow_rate_category": obs.flow_rate_category,
                "odor": obs.odor,
                "algae_coverage_pct": obs.algae_coverage_pct,
                "canopy_cover_pct": obs.canopy_cover_pct,
                "litter_present": obs.litter_present,
                "flags": obs.assessment.flags if obs.assessment else [],
            },
            created_at=_utcnow(),
        )
        nodes.append(obs_node)
        obs_nodes_map[obs.id] = obs_node

        edges.append(
            EvidenceEdge(
                id=f"edge:{obs_node_id}->{site_node_id}",
                source_node_id=obs_node_id,
                target_node_id=site_node_id,
                edge_type="located_at",
                weight=1.0,
                reason="Observation recorded at site location",
                created_at=_utcnow(),
            )
        )

    # Measurement Nodes & Edges
    meas_nodes_map: dict[str, EvidenceNode] = {}
    for m in measurements:
        meas_node_id = f"node:meas:{m.id}"
        meas_node = EvidenceNode(
            id=meas_node_id,
            node_type="MEASUREMENT",
            label=f"{m.parameter}: {m.value} {m.unit}",
            description=f"Quantitative measurement of {m.parameter} with flag {m.quality_flag}",
            confidence=0.95 if m.quality_flag == "good" else 0.5,
            source_reference=f"measurements/{m.id}",
            properties={
                "observed_at": m.observed_at.isoformat() if m.observed_at else None,
                "parameter": m.parameter,
                "value": m.value,
                "unit": m.unit,
                "quality_flag": m.quality_flag,
            },
            created_at=_utcnow(),
        )
        nodes.append(meas_node)
        meas_nodes_map[m.id] = meas_node

        edges.append(
            EvidenceEdge(
                id=f"edge:{meas_node_id}->{site_node_id}",
                source_node_id=meas_node_id,
                target_node_id=site_node_id,
                edge_type="located_at",
                weight=1.0,
                reason="In-situ sensor or lab measurement at site",
                created_at=_utcnow(),
            )
        )

    # EO Measurement Nodes & Edges
    eo_nodes_map: dict[str, EvidenceNode] = {}
    for eo in eo_measurements:
        eo_node_id = f"node:eo:{eo.id}"
        eo_node = EvidenceNode(
            id=eo_node_id,
            node_type="EO_SIGNAL",
            label=f"{eo.satellite_source} (NDVI: {eo.ndvi}, NDWI: {eo.ndwi})",
            description=f"Remote sensing: NDVI={eo.ndvi}, NDWI={eo.ndwi}, surface_temp={eo.surface_temp_c}°C",
            confidence=0.90 if (eo.cloud_cover_pct or 0) < 20 else 0.60,
            source_reference=f"eo_measurements/{eo.id}",
            properties={
                "observed_at": eo.observed_at.isoformat() if eo.observed_at else None,
                "satellite_source": eo.satellite_source,
                "ndvi": eo.ndvi,
                "ndwi": eo.ndwi,
                "surface_temp_c": eo.surface_temp_c,
                "cloud_cover_pct": eo.cloud_cover_pct,
            },
            created_at=_utcnow(),
        )
        nodes.append(eo_node)
        eo_nodes_map[eo.id] = eo_node

        edges.append(
            EvidenceEdge(
                id=f"edge:{eo_node_id}->{site_node_id}",
                source_node_id=eo_node_id,
                target_node_id=site_node_id,
                edge_type="located_at",
                weight=0.9,
                reason="Satellite earth observation coverage",
                created_at=_utcnow(),
            )
        )

    # 5. Cross-modal Relationship Inference (Supports / Contradicts / Correlates)
    edge_count = len(edges)
    for obs in observations:
        obs_node_id = f"node:obs:{obs.id}"

        # Check against measurements
        for m in measurements:
            meas_node_id = f"node:meas:{m.id}"
            param = m.parameter.lower()

            # Water clarity vs Turbidity
            if param == "turbidity":
                if obs.water_clarity == "clear" and m.value > 20.0:
                    edges.append(
                        EvidenceEdge(
                            id=f"edge:contradict:{obs_node_id}:{meas_node_id}",
                            source_node_id=obs_node_id,
                            target_node_id=meas_node_id,
                            edge_type="contradicts",
                            weight=0.85,
                            reason=f"Observer reported clear water but measured turbidity is elevated ({m.value} NTU)",
                            created_at=_utcnow(),
                        )
                    )
                elif obs.water_clarity == "turbid" and m.value > 15.0:
                    edges.append(
                        EvidenceEdge(
                            id=f"edge:supports:{obs_node_id}:{meas_node_id}",
                            source_node_id=obs_node_id,
                            target_node_id=meas_node_id,
                            edge_type="supports",
                            weight=0.90,
                            reason=f"Turbid visual observation corroborated by high turbidity measurement ({m.value} NTU)",
                            created_at=_utcnow(),
                        )
                    )

            # Odor / Algae vs Dissolved Oxygen
            if param == "dissolved_oxygen":
                if obs.odor == "sewage" and m.value < 4.0:
                    edges.append(
                        EvidenceEdge(
                            id=f"edge:supports:{obs_node_id}:{meas_node_id}",
                            source_node_id=obs_node_id,
                            target_node_id=meas_node_id,
                            edge_type="supports",
                            weight=0.92,
                            reason=f"Sewage odor is corroborated by hypoxic dissolved oxygen ({m.value} mg/L)",
                            created_at=_utcnow(),
                        )
                    )
                elif obs.odor == "sewage" and m.value > 8.0:
                    edges.append(
                        EvidenceEdge(
                            id=f"edge:contradict:{obs_node_id}:{meas_node_id}",
                            source_node_id=obs_node_id,
                            target_node_id=meas_node_id,
                            edge_type="contradicts",
                            weight=0.75,
                            reason=f"Sewage odor reported but dissolved oxygen is well saturated ({m.value} mg/L)",
                            created_at=_utcnow(),
                        )
                    )

            # Algae coverage vs Nitrate
            if param == "nitrate" and obs.algae_coverage_pct is not None:
                if obs.algae_coverage_pct > 30 and m.value > 5.0:
                    edges.append(
                        EvidenceEdge(
                            id=f"edge:supports:{obs_node_id}:{meas_node_id}",
                            source_node_id=obs_node_id,
                            target_node_id=meas_node_id,
                            edge_type="supports",
                            weight=0.88,
                            reason=f"High algae coverage ({obs.algae_coverage_pct}%) correlates with elevated nitrate ({m.value} mg/L)",
                            created_at=_utcnow(),
                        )
                    )

        # Check against EO
        for eo in eo_measurements:
            eo_node_id = f"node:eo:{eo.id}"
            if eo.ndvi is not None and obs.canopy_cover_pct is not None:
                if eo.ndvi > 0.5 and obs.canopy_cover_pct > 50:
                    edges.append(
                        EvidenceEdge(
                            id=f"edge:supports:{obs_node_id}:{eo_node_id}",
                            source_node_id=obs_node_id,
                            target_node_id=eo_node_id,
                            edge_type="supports",
                            weight=0.85,
                            reason=f"Visual canopy cover ({obs.canopy_cover_pct}%) aligns with satellite NDVI ({eo.ndvi:.2f})",
                            created_at=_utcnow(),
                        )
                    )
                elif eo.ndvi < 0.25 and obs.canopy_cover_pct > 60:
                    edges.append(
                        EvidenceEdge(
                            id=f"edge:contradict:{obs_node_id}:{eo_node_id}",
                            source_node_id=obs_node_id,
                            target_node_id=eo_node_id,
                            edge_type="contradicts",
                            weight=0.70,
                            reason=f"Observer noted dense canopy ({obs.canopy_cover_pct}%) but EO NDVI is low ({eo.ndvi:.2f})",
                            created_at=_utcnow(),
                        )
                    )

    if persist:
        # Save or merge nodes and edges in DB
        for node in nodes:
            await db.merge(node)
        for edge in edges:
            await db.merge(edge)
        await db.commit()

    return {
        "nodes": nodes,
        "edges": edges,
    }
