"""Integration tests for Stream Fingerprints and Twin Engine."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete

from aquarys.core.database import async_session_maker, init_db
from aquarys.main import app
from aquarys.models import StreamEmbedding, StreamProfile
from aquarys.services.fingerprints.builder import build_fingerprint


@pytest.mark.asyncio
async def test_fingerprint_builder():
    """Test generating fingerprint from raw data maps correctly."""
    await init_db()

    # Build dummy DB context
    async with async_session_maker():
        # Just use the builder's internal logic, skip inserting raw rows for pure logic test
        # We simulate what the DB fetch would return

        # Test 1: Empty context
        profile_empty = build_fingerprint({}, [], [], [])
        assert profile_empty["water_quality_score"] is None
        assert profile_empty["data_coverage_pct"] == 0.0

        # In a real integration test, we'd insert OAH data here.
        # But this suffices to check the pipeline doesn't crash on empty.


@pytest.mark.asyncio
async def test_twins_api_search():
    """Test POST /twins/search and GET /twins/{a}/{b}."""
    await init_db()

    async with async_session_maker() as session:
        # Clean up any existing test data
        await session.execute(delete(StreamEmbedding))
        await session.execute(delete(StreamProfile))
        await session.commit()

        import uuid

        uid = uuid.uuid4().hex[:8]
        sa = f"site_a_{uid}"
        sb = f"site_b_{uid}"
        sc = f"site_c_{uid}"

        # Inject mock profiles & embeddings
        p1 = StreamProfile(
            site_id=sa, water_quality_score=90.0, habitat_score=80.0, data_coverage_pct=80.0
        )
        e1 = StreamEmbedding(site_id=sa, vector=[0.1, 0.2, 0.3])

        p2 = StreamProfile(
            site_id=sb, water_quality_score=85.0, habitat_score=75.0, data_coverage_pct=80.0
        )
        e2 = StreamEmbedding(site_id=sb, vector=[0.15, 0.2, 0.25])

        p3 = StreamProfile(
            site_id=sc, water_quality_score=10.0, habitat_score=10.0, data_coverage_pct=80.0
        )
        e3 = StreamEmbedding(site_id=sc, vector=[-0.9, -0.8, -0.7])

        session.add_all([p1, e1, p2, e2, p3, e3])
        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Search with min_similarity=0.0
        payload = {"target_site_id": sa, "limit": 2, "min_similarity": 0.0}
        resp = await client.post("/twins/search", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        assert data[0]["site_b_id"] == sb

        # Direct comparison
        resp2 = await client.get(f"/twins/{sa}/{sb}")
        assert resp2.status_code == 200
        data2 = resp2.json()
        assert data2["overall_similarity"] > 0.7

        resp3 = await client.get(f"/twins/{sa}/site_missing")
        assert resp3.status_code == 404

        # Cleanup
        async with async_session_maker() as cleanup:
            await cleanup.execute(delete(StreamEmbedding))
            await cleanup.execute(delete(StreamProfile))
            await cleanup.commit()
