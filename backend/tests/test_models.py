"""Test database schema creation and model operations."""

import uuid
from datetime import datetime, timezone
import pytest
from sqlalchemy import select
from aquarys.core.database import init_db, async_session_maker
from aquarys.models import Site, Observation, StreamProfile, StreamEmbedding, Mission, MissionTask


@pytest.mark.asyncio
async def test_database_models():
    await init_db()
    test_id = f"PT-COI-{uuid.uuid4().hex[:6]}"
    async with async_session_maker() as session:
        # Create test site
        site = Site(
            id=test_id,
            code="C1",
            name="Ribeira de Coselhas",
            city="Coimbra",
            country="Portugal",
            stream_name="Coselhas",
            latitude=40.2251,
            longitude=-8.4312,
            is_hero=True,
            description="Urban stream segment experiencing riparian degradation and runoff.",
            source="OAH",
        )
        session.add(site)
        await session.commit()

        # Query site back
        stmt = select(Site).where(Site.id == test_id)
        result = await session.execute(stmt)
        queried_site = result.scalar_one_or_none()
        assert queried_site is not None
        assert queried_site.code == "C1"
        assert queried_site.is_hero is True

        # Add observation & stream profile
        obs = Observation(
            id=f"OBS-{uuid.uuid4().hex[:6]}",
            site_id=site.id,
            observed_at=datetime.now(timezone.utc),
            latitude=40.2251,
            longitude=-8.4312,
            water_clarity="turbid",
            notes="Turbid water observed after rain event.",
        )
        profile = StreamProfile(
            site_id=site.id,
            water_quality_score=58.5,
            habitat_score=42.0,
            vegetation_score=45.0,
            hydromorphology_score=31.0,
            biotics_score=55.0,
            nutrients_score=68.0,
            citizen_evidence_score=91.0,
            data_coverage_pct=88.5,
            evidence_confidence_pct=86.0,
        )
        emb = StreamEmbedding(
            site_id=site.id,
            vector=[0.1, 0.2, 0.3, 0.4, 0.5],
        )
        session.add_all([obs, profile, emb])
        await session.commit()

        # Verify query with relationship
        stmt_prof = select(StreamProfile).where(StreamProfile.site_id == test_id)
        res_prof = (await session.execute(stmt_prof)).scalar_one_or_none()
        assert res_prof is not None
        assert res_prof.water_quality_score == 58.5
