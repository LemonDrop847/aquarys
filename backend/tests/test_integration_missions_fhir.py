"""Integration tests for Knowledge Gaps, Mission Optimizer, and FHIR Export."""

from datetime import UTC, datetime

import pytest
from httpx import ASGITransport, AsyncClient

from aquarys.core.database import Base, engine, get_db
from aquarys.main import app
from aquarys.models import (
    EOMeasurement,
    Measurement,
    Observation,
    OracleInvestigation,
    Site,
    StreamProfile,
)
from aquarys.services.fhir.exporter import export_investigation_to_fhir_bundle
from aquarys.services.missions.gaps import detect_knowledge_gaps
from aquarys.services.missions.information_gain import calculate_dimension_information_gain
from aquarys.services.missions.optimizer import optimize_mission


@pytest.fixture(autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_missions_and_fhir_export_pipeline():
    async for db in get_db():
        # Seed test site with telemetry and profile
        site = Site(
            id="site_mission_test",
            code="SMT-01",
            name="Ribeira de Alcantara Mission Reach",
            city="Lisbon",
            country="Portugal",
            latitude=38.73,
            longitude=-9.18,
            altitude_m=24.0,
            description="Urban stream reach undergoing ecological monitoring.",
        )
        profile = StreamProfile(
            site_id="site_mission_test",
            water_quality_score=45.0,
            habitat_score=50.0,
            vegetation_score=40.0,
            hydromorphology_score=35.0,
            data_coverage_pct=60.0,
            evidence_confidence_pct=70.0,
            dimension_status={
                "water_quality": "observed",
                "macroinvertebrates": "missing",
                "nutrients": "estimated",
                "vegetation": "missing",
            },
        )
        obs1 = Observation(
            id="obs_m_01",
            site_id="site_mission_test",
            latitude=38.73,
            longitude=-9.18,
            observed_at=datetime.now(UTC),
            water_clarity="turbid",
            odor="sulfur",
            algae_coverage_pct=30.0,
            canopy_cover_pct=25.0,
        )
        meas_do = Measurement(
            id="meas_m_do",
            site_id="site_mission_test",
            parameter="dissolved_oxygen",
            value=3.4,
            unit="mg/L",
            observed_at=datetime.now(UTC),
        )
        meas_turb = Measurement(
            id="meas_m_turb",
            site_id="site_mission_test",
            parameter="turbidity",
            value=24.0,
            unit="NTU",
            observed_at=datetime.now(UTC),
        )
        meas_nitrate = Measurement(
            id="meas_m_nitrate",
            site_id="site_mission_test",
            parameter="nitrate",
            value=7.8,
            unit="mg/L",
            observed_at=datetime.now(UTC),
        )
        eo = EOMeasurement(
            id="eo_m_01",
            site_id="site_mission_test",
            satellite_source="Sentinel-2",
            ndvi=0.45,
            ndwi=0.12,
            observed_at=datetime.now(UTC),
        )

        db.add_all([site, profile, obs1, meas_do, meas_turb, meas_nitrate, eo])
        await db.commit()

        # Seed Oracle Investigation for FHIR export
        inv = OracleInvestigation(
            id="inv_test_fhir_01",
            site_id="site_mission_test",
            question="What is causing the severe oxygen depletion and sulfur odor?",
            finding="Untreated stormwater runoff and elevated organic nutrient loading.",
            facts=["Dissolved Oxygen is 3.4 mg/L", "Turbidity is 24.0 NTU"],
            hypotheses=[
                {
                    "statement": "Episodic sewage ingress is driving organic microbial decomposition.",
                    "plausibility_score": 0.88,
                    "supporting_evidence_ids": ["obs_m_01", "meas_m_do"],
                    "counter_evidence": "None recorded in current window",
                    "skeptic_challenge": "Could temperature anomalies explain the lower oxygen solubility?",
                    "remaining_uncertainty": "Requires upstream ammonium and microbial assay confirmation.",
                }
            ],
            counter_evidence=["No industrial discharge permitted in catchment"],
            data_gaps=[{"dimension": "macroinvertebrates", "gap": "Absence of bio-indicator taxa"}],
            next_observations=[{"task": "Deploy volunteer kick-net survey"}],
            caveats=["Single daytime observation window"],
            evidence_ids=["obs_m_01", "meas_m_do", "meas_m_turb", "meas_m_nitrate"],
            activity_events=[{"step": "synthesis", "timestamp": datetime.now(UTC).isoformat()}],
            provider_used="demo",
        )
        db.add(inv)
        await db.commit()

        # 1. Test Knowledge Gap Detection
        gaps = await detect_knowledge_gaps(db, "site_mission_test")
        assert len(gaps) >= 2
        gap_dims = [g["dimension"] for g in gaps]
        assert "macroinvertebrates" in gap_dims

        # 2. Test Information Gain
        gain = await calculate_dimension_information_gain(
            db, "site_mission_test", "macroinvertebrates"
        )
        assert gain["expected_information_gain"] > 0.3
        assert gain["prior_uncertainty"] > gain["expected_posterior_uncertainty"]

        # 3. Test Mission Optimizer Service
        mission_dict = await optimize_mission(
            db=db,
            site_id="site_mission_test",
            volunteer_count=4,
            available_time_minutes=60,
            persist=True,
        )
        assert mission_dict["volunteer_count"] == 4
        assert len(mission_dict["tasks"]) == 4
        assert mission_dict["expected_information_gain"] > 0.2
        assert len(mission_dict["gaps_addressed"]) >= 1

        # 4. Test FHIR Exporter Service
        fhir_bundle = await export_investigation_to_fhir_bundle(db, "inv_test_fhir_01")
        assert fhir_bundle["resourceType"] == "Bundle"
        assert fhir_bundle["type"] == "document"
        assert len(fhir_bundle["entry"]) >= 4

        # Verify entry resources
        resource_types = [e["resource"]["resourceType"] for e in fhir_bundle["entry"]]
        assert "DiagnosticReport" in resource_types
        assert "Location" in resource_types
        assert "Observation" in resource_types
        assert "RiskAssessment" in resource_types

    # 5. Test REST Endpoints
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Gaps API
        gaps_resp = await ac.get("/missions/gaps/site_mission_test")
        assert gaps_resp.status_code == 200
        gaps_json = gaps_resp.json()
        assert gaps_json["gap_count"] >= 2

        # Gain API
        gain_resp = await ac.get("/missions/gain/site_mission_test/macroinvertebrates")
        assert gain_resp.status_code == 200
        assert gain_resp.json()["expected_information_gain"] > 0.3

        # Optimize Mission API
        opt_resp = await ac.post(
            "/missions/optimize",
            json={
                "site_id": "site_mission_test",
                "volunteer_count": 3,
                "available_time_minutes": 45,
            },
        )
        assert opt_resp.status_code == 200
        opt_json = opt_resp.json()
        assert opt_json["volunteer_count"] == 3
        assert len(opt_json["tasks"]) == 3
        created_mission_id = opt_json["id"]

        # Get Mission by ID API
        get_m_resp = await ac.get(f"/missions/{created_mission_id}")
        assert get_m_resp.status_code == 200
        assert get_m_resp.json()["id"] == created_mission_id

        # List Missions API
        list_m_resp = await ac.get("/missions?site_id=site_mission_test")
        assert list_m_resp.status_code == 200
        assert len(list_m_resp.json()) >= 1

        # FHIR Export API
        fhir_resp = await ac.get("/exports/fhir/inv_test_fhir_01")
        assert fhir_resp.status_code == 200
        fhir_json = fhir_resp.json()
        assert fhir_json["resourceType"] == "Bundle"
        assert fhir_json["entry"][0]["resource"]["resourceType"] == "DiagnosticReport"
        assert (
            fhir_json["entry"][0]["resource"]["conclusion"]
            == "Untreated stormwater runoff and elevated organic nutrient loading."
        )
