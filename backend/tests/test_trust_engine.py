"""Integration tests for Trust Engine and Trust API."""

import pytest
from httpx import ASGITransport, AsyncClient

from aquarys.main import app
from aquarys.services.trust.evaluator import EvidenceProfile, evaluate_observation_trust


# --- Unit-level: evaluator directly ---


def _make_observation(**overrides):
    base = {
        "id": "obs-test-01",
        "site_id": "site-01",
        "observer_id": "user-A",
        "observed_at": "2024-06-15T10:30:00Z",
        "latitude": 38.7223,
        "longitude": -9.1393,
        "water_clarity": "clear",
        "flow_rate_category": "moderate",
        "odor": "none",
        "algae_coverage_pct": 5,
        "litter_present": False,
        "canopy_cover_pct": 40,
        "image_urls": ["https://example.com/photo1.jpg", "https://example.com/photo2.jpg"],
        "notes": "Clear water, moderate flow.",
    }
    base.update(overrides)
    return base


def test_evaluator_complete_observation():
    obs = _make_observation()
    profile = evaluate_observation_trust(obs)
    assert isinstance(profile, EvidenceProfile)
    assert 0.0 <= profile.overall_confidence <= 1.0
    assert profile.completeness > 0.7
    assert profile.consistency > 0.5
    assert profile.image_support >= 0.8
    assert "LOW_COMPLETENESS" not in profile.flags


def test_evaluator_sparse_observation():
    obs = _make_observation(
        water_clarity=None,
        flow_rate_category=None,
        odor=None,
        algae_coverage_pct=None,
        image_urls=[],
        notes=None,
    )
    profile = evaluate_observation_trust(obs)
    assert profile.completeness < 0.6
    assert profile.image_support < 0.4
    assert "LOW_COMPLETENESS" in profile.flags
    assert "UNVERIFIED_VISUAL" in profile.flags


def test_evaluator_with_corroborating_observations():
    obs = _make_observation()
    other = _make_observation(
        id="obs-test-02",
        observer_id="user-B",
        observed_at="2024-06-15T12:00:00Z",
    )
    profile = evaluate_observation_trust(obs, existing_observations=[other])
    assert profile.cross_observer >= 0.6
    assert any("Cross-corroborated" in s for s in profile.positive_signals)


def test_evaluator_with_sensor_measurements():
    obs = _make_observation(water_clarity="clear")
    measurements = [{"parameter_name": "turbidity", "value": 3.0, "unit": "NTU"}]
    profile = evaluate_observation_trust(obs, measurements=measurements)
    assert profile.independent_support > 0.5
    assert any("Turbidity probe" in s for s in profile.positive_signals)


def test_evaluator_duplicate_risk_penalizes_confidence():
    obs = _make_observation()
    # Same observer, same time, same location = duplicate
    dupe = _make_observation(id="obs-test-dupe", observer_id="user-A")
    profile = evaluate_observation_trust(obs, existing_observations=[dupe])
    assert profile.duplicate_risk > 0.0


def test_evaluator_overall_confidence_in_range():
    """Confidence always [0, 1] regardless of inputs."""
    for kwargs in [
        {},
        {"water_clarity": None, "image_urls": []},
        {"latitude": None, "longitude": None},
    ]:
        obs = _make_observation(**kwargs)
        profile = evaluate_observation_trust(obs)
        assert 0.0 <= profile.overall_confidence <= 1.0


# --- API-level: POST /trust/evaluate with ad-hoc data ---


@pytest.mark.asyncio
async def test_trust_evaluate_adhoc():
    """POST /trust/evaluate with inline observation_data (no DB required)."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "observation_id": None,
            "observation_data": _make_observation(),
            "persist": False,
        }
        resp = await client.post("/trust/evaluate", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "overall_confidence" in data
        assert 0.0 <= data["overall_confidence"] <= 1.0
        assert "completeness" in data
        assert "flags" in data
        assert data["observation_id"] == "adhoc"
