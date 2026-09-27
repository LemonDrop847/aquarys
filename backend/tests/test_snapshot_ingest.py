"""Tests for snapshot ingestion."""

from pathlib import Path
from aquarys.services.ingestion.snapshot import SnapshotIngestionService


def test_snapshot_ingest_all(tmp_path: Path):
    snapshots_dir = Path(__file__).parents[1] / "data" / "snapshots"
    service = SnapshotIngestionService(snapshots_dir=snapshots_dir, raw_dir=tmp_path)

    results = service.ingest_all_snapshots()

    assert "sites" in results
    assert "observations" in results
    assert "measurements" in results
    assert "eo_measurements" in results

    assert results["sites"]["count"] >= 5
    assert results["observations"]["count"] >= 5
    assert len(results["sites"]["payload_hash"]) == 64
    assert Path(results["sites"]["raw_storage_path"]).exists()
