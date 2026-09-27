"""Tests for canonical data normalization."""

from aquarys.services.normalization import CanonicalNormalizer, normalize_site, normalize_observation, normalize_measurement, normalize_eo_measurement
from aquarys.services.ingestion.snapshot import SnapshotIngestionService


def test_normalize_snapshots():
    service = SnapshotIngestionService()
    snapshots = service.ingest_all_snapshots()

    # Sites
    sites_raw = snapshots["sites"]["items"]
    norm_sites = CanonicalNormalizer.normalize_batch("sites", sites_raw, snapshots["sites"]["payload_hash"])
    assert len(norm_sites) == len(sites_raw)
    first_site = norm_sites[0]
    assert first_site["id"] == "PT-COI-01"
    assert first_site["city"] == "Coimbra"
    assert first_site["raw_payload_hash"] == snapshots["sites"]["payload_hash"]
    assert "hydrological_basin" in first_site["metadata_json"]  # preserved extra field

    # Observations
    obs_raw = snapshots["observations"]["items"]
    norm_obs = CanonicalNormalizer.normalize_batch("observations", obs_raw, snapshots["observations"]["payload_hash"])
    assert len(norm_obs) == len(obs_raw)
    first_obs = norm_obs[0]
    assert first_obs["site_id"] == "PT-COI-01"
    assert "water_color" in first_obs["metadata_json"]  # preserved extra metadata

    # Measurements
    meas_raw = snapshots["measurements"]["items"]
    norm_meas = CanonicalNormalizer.normalize_batch("measurements", meas_raw, snapshots["measurements"]["payload_hash"])
    assert len(norm_meas) == len(meas_raw)
    first_meas = norm_meas[0]
    assert first_meas["parameter"] == "dissolved_oxygen"
    assert first_meas["value"] == 4.8
    assert "calibration_date" in first_meas["metadata_json"]

    # EO Measurements
    eo_raw = snapshots["eo_measurements"]["items"]
    norm_eo = CanonicalNormalizer.normalize_batch("eo_measurements", eo_raw, snapshots["eo_measurements"]["payload_hash"])
    assert len(norm_eo) == len(eo_raw)
    first_eo = norm_eo[0]
    assert first_eo["satellite_source"] == "Sentinel-2"
    assert first_eo["ndvi"] == 0.41


def test_to_sqlalchemy_models():
    site_model = CanonicalNormalizer.to_site_model({
        "id": "TEST-01",
        "name": "Test River Site",
        "latitude": 40.2,
        "longitude": -8.4,
        "extra_custom_prop": "custom_val"
    })
    assert site_model.id == "TEST-01"
    assert site_model.metadata_json["extra_custom_prop"] == "custom_val"

    obs_model = CanonicalNormalizer.to_observation_model({
        "id": "OBS-01",
        "site_id": "TEST-01",
        "latitude": 40.2,
        "longitude": -8.4,
        "water_clarity": "turbid"
    })
    assert obs_model.water_clarity == "turbid"

    meas_model = CanonicalNormalizer.to_measurement_model({
        "id": "MEA-01",
        "site_id": "TEST-01",
        "parameter": "ph",
        "value": 7.4,
        "unit": "pH"
    })
    assert meas_model.parameter == "ph"
    assert meas_model.value == 7.4

    eo_model = CanonicalNormalizer.to_eo_measurement_model({
        "id": "EO-01",
        "site_id": "TEST-01",
        "band_or_index": "NDWI",
        "mean_value": -0.15
    })
    assert eo_model.ndwi == -0.15
