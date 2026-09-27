"""Test Site and Observation APIs."""

import pytest
from httpx import ASGITransport, AsyncClient

from aquarys.core.database import async_session_maker, init_db
from aquarys.main import app
from aquarys.services.ingestion.snapshot import SnapshotIngestionService
from aquarys.services.normalization import CanonicalNormalizer


@pytest.mark.asyncio
async def test_sites_and_observations_api():
    await init_db()

    # Ingest snapshots and insert into db
    service = SnapshotIngestionService()
    snapshots = service.ingest_all_snapshots()

    async with async_session_maker() as session:
        # Sites
        sites_raw = snapshots["sites"]["items"]
        norm_sites = CanonicalNormalizer.normalize_batch(
            "sites", sites_raw, snapshots["sites"]["payload_hash"]
        )
        for s in norm_sites:
            site_obj = CanonicalNormalizer.to_site_model(s)
            await session.merge(site_obj)

        # Observations
        obs_raw = snapshots["observations"]["items"]
        norm_obs = CanonicalNormalizer.normalize_batch(
            "observations", obs_raw, snapshots["observations"]["payload_hash"]
        )
        for o in norm_obs:
            obs_obj = CanonicalNormalizer.to_observation_model(o)
            await session.merge(obs_obj)

        # Measurements
        meas_raw = snapshots["measurements"]["items"]
        norm_meas = CanonicalNormalizer.normalize_batch(
            "measurements", meas_raw, snapshots["measurements"]["payload_hash"]
        )
        for m in norm_meas:
            meas_obj = CanonicalNormalizer.to_measurement_model(m)
            await session.merge(meas_obj)

        # EO Measurements
        eo_raw = snapshots["eo_measurements"]["items"]
        norm_eo = CanonicalNormalizer.normalize_batch(
            "eo_measurements", eo_raw, snapshots["eo_measurements"]["payload_hash"]
        )
        for eo in norm_eo:
            eo_obj = CanonicalNormalizer.to_eo_measurement_model(eo)
            await session.merge(eo_obj)

        await session.commit()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. GET /sites
        res = await client.get("/sites")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] > 0
        assert len(data["items"]) > 0

        first_site = data["items"][0]
        site_id = first_site["id"]

        # 2. GET /sites/{id}
        res_site = await client.get(f"/sites/{site_id}")
        assert res_site.status_code == 200
        site_data = res_site.json()
        assert site_data["id"] == site_id
        assert site_data["city"] in ["Coimbra", "Ghent", "Lisbon"]

        # 3. GET /sites/{id}/timeline
        res_timeline = await client.get(f"/sites/{site_id}/timeline")
        assert res_timeline.status_code == 200
        timeline_data = res_timeline.json()
        assert timeline_data["site_id"] == site_id
        assert "events" in timeline_data

        # 4. GET /observations
        res_obs = await client.get("/observations")
        assert res_obs.status_code == 200
        obs_data = res_obs.json()
        assert obs_data["total"] > 0
        first_obs = obs_data["items"][0]
        obs_id = first_obs["id"]

        # 5. GET /observations/{id}
        res_obs_single = await client.get(f"/observations/{obs_id}")
        assert res_obs_single.status_code == 200
        single_obs_data = res_obs_single.json()
        assert single_obs_data["id"] == obs_id
        assert single_obs_data["site_id"] is not None

        # 6. GET /sites/nonexistent -> 404
        res_404 = await client.get("/sites/NONEXISTENT-SITE")
        assert res_404.status_code == 404
