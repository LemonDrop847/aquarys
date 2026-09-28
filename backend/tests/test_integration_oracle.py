"""Integration tests for Evidence Graph, Deterministic Tools, and Grounded Oracle."""

from datetime import UTC, datetime
import pytest
from httpx import ASGITransport, AsyncClient

from aquarys.core.database import Base, engine, get_db
from aquarys.main import app
from aquarys.models import (
    EOMeasurement,
    Measurement,
    Observation,
    Site,
    StreamProfile,
)
from aquarys.services.graph.builder import build_evidence_graph_for_site
from aquarys.services.oracle.tools import (
    tool_calculate_information_gain,
    tool_find_corroborating_evidence,
    tool_get_evidence,
    tool_get_interventions,
)


@pytest.fixture(autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_evidence_graph_and_oracle_pipeline():
    async for db in get_db():
        # Seed test site with multi-modal data designed to trigger supports & contradictions
        site = Site(
            id="site_oracle_test",
            code="SOT-01",
            name="Ribeira de Alcantara Oracle Reach",
            city="Lisbon",
            country="Portugal",
            latitude=38.72,
            longitude=-9.17,
        )
        profile = StreamProfile(
            site_id="site_oracle_test",
            water_quality_score=42.0,
            habitat_score=48.0,
            vegetation_score=55.0,
            hydromorphology_score=35.0,
            data_coverage_pct=75.0,
            dimension_status={
                "water_quality": "observed",
                "macroinvertebrates": "missing",
                "nutrients": "estimated",
            },
        )
        obs_clear = Observation(
            id="obs_clear_contradict",
            site_id="site_oracle_test",
            latitude=38.72,
            longitude=-9.17,
            observed_at=datetime.now(UTC),
            water_clarity="clear",
            odor="none",
            canopy_cover_pct=70.0,
        )
        obs_sewage = Observation(
            id="obs_sewage_support",
            site_id="site_oracle_test",
            latitude=38.72,
            longitude=-9.17,
            observed_at=datetime.now(UTC),
            water_clarity="turbid",
            odor="sewage",
            algae_coverage_pct=45.0,
        )
        meas_turb = Measurement(
            id="meas_turb_high",
            site_id="site_oracle_test",
            parameter="turbidity",
            value=28.5,
            unit="NTU",
            observed_at=datetime.now(UTC),
        )
        meas_do = Measurement(
            id="meas_do_low",
            site_id="site_oracle_test",
            parameter="dissolved_oxygen",
            value=2.8,
            unit="mg/L",
            observed_at=datetime.now(UTC),
        )
        meas_nitrate = Measurement(
            id="meas_nitrate_high",
            site_id="site_oracle_test",
            parameter="nitrate",
            value=8.4,
            unit="mg/L",
            observed_at=datetime.now(UTC),
        )
        eo = EOMeasurement(
            id="eo_signal_01",
            site_id="site_oracle_test",
            satellite_source="Sentinel-2",
            ndvi=0.62,
            ndwi=0.15,
            observed_at=datetime.now(UTC),
        )

        db.add_all([site, profile, obs_clear, obs_sewage, meas_turb, meas_do, meas_nitrate, eo])
        await db.commit()

        # Test 1: Relational Graph Builder directly
        graph = await build_evidence_graph_for_site(db, "site_oracle_test", persist=False)
        assert len(graph["nodes"]) >= 6
        assert len(graph["edges"]) >= 5

        edge_types = [e.edge_type for e in graph["edges"]]
        assert "contradicts" in edge_types
        assert "supports" in edge_types

        # Test 2: Deterministic Tools
        evidence_dict = await tool_get_evidence(db, "site_oracle_test")
        assert len(evidence_dict["contradictions"]) >= 1
        assert len(evidence_dict["supports"]) >= 1

        corrob = await tool_find_corroborating_evidence(db, "obs_sewage_support")
        assert "site_id" in corrob
        assert len(corrob["supporting_reasons"]) >= 1

        interventions = await tool_get_interventions(db, "site_oracle_test")
        assert len(interventions) >= 2

        gain = await tool_calculate_information_gain(db, "site_oracle_test", "macroinvertebrates")
        assert gain["expected_information_gain"] > 0.30

    # Test 3: FastAPI Oracle API Endpoints
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Graph API
        g_resp = await ac.get("/evidence/graph/site_oracle_test")
        assert g_resp.status_code == 200
        g_data = g_resp.json()
        assert g_data["node_count"] >= 6
        assert g_data["contradiction_count"] >= 1

        # Investigate API
        inv_resp = await ac.post(
            "/oracle/investigate",
            json={
                "site_id": "site_oracle_test",
                "question": "Assess biological degradation and nutrient loading drivers.",
                "provider": "demo",
            },
        )
        assert inv_resp.status_code == 200
        inv_data = inv_resp.json()
        assert "id" in inv_data
        assert "finding" in inv_data
        assert len(inv_data["hypotheses"]) >= 1
        assert len(inv_data["facts"]) >= 2
        assert len(inv_data["activity_events"]) >= 4

        investigation_id = inv_data["id"]

        # Fetch Investigation by ID
        get_inv = await ac.get(f"/oracle/investigations/{investigation_id}")
        assert get_inv.status_code == 200
        assert get_inv.json()["id"] == investigation_id

        # Skeptic Challenge API
        chal_resp = await ac.post(
            "/oracle/challenge",
            json={
                "site_id": "site_oracle_test",
                "hypothesis_statement": inv_data["hypotheses"][0]["statement"],
                "provider": "demo",
            },
        )
        assert chal_resp.status_code == 200
        chal_data = chal_resp.json()
        assert chal_data["adjusted_plausibility"] < chal_data["original_plausibility"]
        assert "skeptic_critique" in chal_data
        assert len(chal_data["suggested_verification_test"]) > 10
