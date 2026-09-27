"""Tests for resilient OAH ingestion client."""

import pytest
from pathlib import Path
from aquarys.services.ingestion.client import OAHClient


def test_hash_computation(tmp_path: Path):
    client = OAHClient(raw_storage_dir=tmp_path)
    sample_payload = {"test": 123, "city": "Coimbra"}
    h = client.compute_hash(sample_payload)
    assert isinstance(h, str)
    assert len(h) == 64

    # Identical content yields identical hash
    h2 = client.compute_hash(sample_payload)
    assert h == h2


def test_persist_raw_payload(tmp_path: Path):
    client = OAHClient(raw_storage_dir=tmp_path)
    sample_payload = [{"id": "PT-COI-01", "name": "Ribeira de Coselhas"}]
    payload_hash = client.compute_hash(sample_payload)
    saved_file = client._persist_raw_payload("/sites", sample_payload, payload_hash)

    assert saved_file.exists()
    assert saved_file.is_file()
