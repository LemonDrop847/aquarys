"""Major Integration Test 3: Fingerprints, Embeddings, Twin Engine, and Twin APIs."""

import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from aquarys.core.database import async_session_maker, init_db
from aquarys.main import app
from aquarys.models import Site, StreamEmbedding, StreamProfile, StreamSimilarity
from aquarys.services.fingerprints.builder import (
    build_embedding,
    build_fingerprint,
    cosine_similarity,
)
from aquarys.services.twins.scoring import calculate_twin_similarity


@pytest.mark.asyncio
async def test_integration_fingerprint_to_twin_pipeline():
    """End-to-end integration test: raw data -> fingerprint -> embedding -> DB -> API search & comparison."""
    await init_db()

    run_id = uuid.uuid4().hex[:6]
    site_lisbon_id = f"PT-LIS-{run_id}"
    site_coimbra_id = f"PT-COI-{run_id}"
    site_ghent_id = f"BE-GNT-{run_id}"

    # 1. Raw Data for Lisbon Site (Healthy, high clarity, moderate DO, high NDVI)
    lisbon_obs = [
        {
            "canopy_cover_pct": 70,
            "litter_present": False,
            "algae_coverage_pct": 5,
            "flow_rate_category": "moderate",
            "water_clarity": "clear",
            "odor": "none",
            "image_urls": ["https://example.com/lis1.jpg"],
        }
    ]
    lisbon_meas = [
        {"parameter": "ph", "value": 7.2},
        {"parameter": "dissolved_oxygen", "value": 9.5},
        {"parameter": "turbidity", "value": 4.0},
        {"parameter": "nitrate", "value": 1.5},
    ]
    lisbon_eo = [{"ndvi": 0.65, "ndwi": 0.2, "surface_temp_c": 18.0, "cloud_cover_pct": 10.0}]

    # Build Lisbon Fingerprint
    fp_lisbon = build_fingerprint(
        site_data={"id": site_lisbon_id},
        observations=lisbon_obs,
        measurements=lisbon_meas,
        eo_data=lisbon_eo,
        trust_scores=[0.92],
    )
    assert fp_lisbon["data_coverage_pct"] == 100.0
    assert fp_lisbon["water_quality_score"] > 80.0
    assert fp_lisbon["habitat_score"] > 80.0
    assert fp_lisbon["dimension_status"]["water_quality_score"] == "observed"

    vec_lisbon = build_embedding(fp_lisbon)
    assert len(vec_lisbon) == 18

    # 2. Raw Data for Coimbra Site (Twin to Lisbon - similar healthy characteristics)
    coimbra_obs = [
        {
            "canopy_cover_pct": 65,
            "litter_present": False,
            "algae_coverage_pct": 8,
            "flow_rate_category": "moderate",
            "water_clarity": "clear",
            "odor": "none",
            "image_urls": ["https://example.com/coi1.jpg"],
        }
    ]
    coimbra_meas = [
        {"parameter": "ph", "value": 7.1},
        {"parameter": "dissolved_oxygen", "value": 9.0},
        {"parameter": "turbidity", "value": 6.0},
        {"parameter": "nitrate", "value": 2.0},
    ]
    coimbra_eo = [{"ndvi": 0.60, "ndwi": 0.18, "surface_temp_c": 19.0, "cloud_cover_pct": 15.0}]

    fp_coimbra = build_fingerprint(
        site_data={"id": site_coimbra_id},
        observations=coimbra_obs,
        measurements=coimbra_meas,
        eo_data=coimbra_eo,
        trust_scores=[0.88],
    )
    vec_coimbra = build_embedding(fp_coimbra)

    # 3. Raw Data for Ghent Site (Degraded stream - low DO, turbid, sewage odor, low NDVI)
    ghent_obs = [
        {
            "canopy_cover_pct": 10,
            "litter_present": True,
            "algae_coverage_pct": 60,
            "flow_rate_category": "stagnant",
            "water_clarity": "turbid",
            "odor": "sewage",
            "image_urls": [],
        }
    ]
    ghent_meas = [
        {"parameter": "ph", "value": 8.8},
        {"parameter": "dissolved_oxygen", "value": 2.5},
        {"parameter": "turbidity", "value": 45.0},
        {"parameter": "nitrate", "value": 12.0},
    ]
    ghent_eo = [{"ndvi": 0.15, "ndwi": -0.1, "surface_temp_c": 26.0, "cloud_cover_pct": 20.0}]

    fp_ghent = build_fingerprint(
        site_data={"id": site_ghent_id},
        observations=ghent_obs,
        measurements=ghent_meas,
        eo_data=ghent_eo,
        trust_scores=[0.60],
    )
    vec_ghent = build_embedding(fp_ghent)

    # Cosine check
    sim_lis_coi = cosine_similarity(vec_lisbon, vec_coimbra)
    sim_lis_gnt = cosine_similarity(vec_lisbon, vec_ghent)
    assert sim_lis_coi > sim_lis_gnt
    assert sim_lis_coi > 0.90

    # 4. Insert Sites, Profiles & Embeddings into DB
    async with async_session_maker() as session:
        s1 = Site(
            id=site_lisbon_id,
            code=f"L_{run_id}",
            name="Lisbon Stream A",
            city="Lisbon",
            country="Portugal",
            latitude=38.72,
            longitude=-9.14,
        )
        s2 = Site(
            id=site_coimbra_id,
            code=f"C_{run_id}",
            name="Coimbra Stream B",
            city="Coimbra",
            country="Portugal",
            latitude=40.20,
            longitude=-8.41,
        )
        s3 = Site(
            id=site_ghent_id,
            code=f"G_{run_id}",
            name="Ghent Stream C",
            city="Ghent",
            country="Belgium",
            latitude=51.05,
            longitude=3.73,
        )

        p1 = StreamProfile(
            site_id=site_lisbon_id,
            water_quality_score=fp_lisbon["water_quality_score"],
            habitat_score=fp_lisbon["habitat_score"],
            vegetation_score=fp_lisbon["vegetation_score"],
            hydromorphology_score=fp_lisbon["hydromorphology_score"],
            biotics_score=fp_lisbon["biotics_score"],
            nutrients_score=fp_lisbon["nutrients_score"],
            eo_context_score=fp_lisbon["eo_context_score"],
            citizen_evidence_score=fp_lisbon["citizen_evidence_score"],
            climate_context_score=fp_lisbon["climate_context_score"],
            dimension_status=fp_lisbon["dimension_status"],
            data_coverage_pct=fp_lisbon["data_coverage_pct"],
            evidence_confidence_pct=fp_lisbon["evidence_confidence_pct"],
        )
        e1 = StreamEmbedding(site_id=site_lisbon_id, vector=vec_lisbon)

        p2 = StreamProfile(
            site_id=site_coimbra_id,
            water_quality_score=fp_coimbra["water_quality_score"],
            habitat_score=fp_coimbra["habitat_score"],
            vegetation_score=fp_coimbra["vegetation_score"],
            hydromorphology_score=fp_coimbra["hydromorphology_score"],
            biotics_score=fp_coimbra["biotics_score"],
            nutrients_score=fp_coimbra["nutrients_score"],
            eo_context_score=fp_coimbra["eo_context_score"],
            citizen_evidence_score=fp_coimbra["citizen_evidence_score"],
            climate_context_score=fp_coimbra["climate_context_score"],
            dimension_status=fp_coimbra["dimension_status"],
            data_coverage_pct=fp_coimbra["data_coverage_pct"],
            evidence_confidence_pct=fp_coimbra["evidence_confidence_pct"],
        )
        e2 = StreamEmbedding(site_id=site_coimbra_id, vector=vec_coimbra)

        p3 = StreamProfile(
            site_id=site_ghent_id,
            water_quality_score=fp_ghent["water_quality_score"],
            habitat_score=fp_ghent["habitat_score"],
            vegetation_score=fp_ghent["vegetation_score"],
            hydromorphology_score=fp_ghent["hydromorphology_score"],
            biotics_score=fp_ghent["biotics_score"],
            nutrients_score=fp_ghent["nutrients_score"],
            eo_context_score=fp_ghent["eo_context_score"],
            citizen_evidence_score=fp_ghent["citizen_evidence_score"],
            climate_context_score=fp_ghent["climate_context_score"],
            dimension_status=fp_ghent["dimension_status"],
            data_coverage_pct=fp_ghent["data_coverage_pct"],
            evidence_confidence_pct=fp_ghent["evidence_confidence_pct"],
        )
        e3 = StreamEmbedding(site_id=site_ghent_id, vector=vec_ghent)

        session.add_all([s1, s2, s3, p1, e1, p2, e2, p3, e3])
        await session.commit()

    # Direct twin scoring calculation test
    sim_calc = calculate_twin_similarity(
        site_a_id=site_lisbon_id,
        profile_a=p1,
        vector_a=vec_lisbon,
        site_b_id=site_coimbra_id,
        profile_b=p2,
        vector_b=vec_coimbra,
    )
    assert sim_calc.overall_similarity > 0.85
    assert len(sim_calc.match_signals) > 0

    # 5. API Testing
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Search for twins of Lisbon
        res = await client.post(
            "/twins/search",
            json={"target_site_id": site_lisbon_id, "limit": 5, "min_similarity": 0.0},
        )
        assert res.status_code == 200
        twins = res.json()
        assert len(twins) == 2
        # Coimbra must rank higher than Ghent
        assert twins[0]["site_b_id"] == site_coimbra_id
        assert twins[0]["overall_similarity"] > twins[1]["overall_similarity"]

        # Differential Comparison Lisbon vs Ghent
        res_comp = await client.get(f"/twins/{site_lisbon_id}/{site_ghent_id}")
        assert res_comp.status_code == 200
        comp_data = res_comp.json()
        assert len(comp_data["differentiators"]) > 0
        assert any("Water Quality" in d for d in comp_data["differentiators"])

    # 6. Cleanup
    async with async_session_maker() as session:
        await session.execute(delete(StreamEmbedding))
        await session.execute(delete(StreamProfile))
        await session.execute(delete(StreamSimilarity))
        await session.execute(delete(Site))
        await session.commit()
