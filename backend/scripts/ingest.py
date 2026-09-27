#!/usr/bin/env python3
"""CLI script to ingest data from OAH API or reproducible local snapshots."""

import argparse
import asyncio
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from aquarys.core.logging import logger
from aquarys.services.ingestion.client import OAHClient
from aquarys.services.ingestion.snapshot import SnapshotIngestionService


async def ingest_live():
    """Ingests live data from configured OAH API."""
    print("Ingesting live data from OAH API...")
    client = OAHClient()
    endpoints = ["/sites", "/observations", "/measurements", "/eo/measurements"]
    for ep in endpoints:
        try:
            res = await client.fetch_endpoint(ep)
            print(f"Ingested {ep}: hash={res['payload_hash'][:8]}")
        except Exception as e:
            logger.warning("Live ingestion failed for %s: %s", ep, e)
            print(f"Skipped {ep}: {e}")


def ingest_snapshot():
    """Ingests reproducible snapshot data."""
    print("Ingesting reproducible data snapshots...")
    service = SnapshotIngestionService()
    results = service.ingest_all_snapshots()
    for entity, res in results.items():
        print(f"Ingested snapshot '{entity}': {res['count']} items (hash={res['payload_hash'][:8]})")
    print("Snapshot ingestion complete.")


def main():
    parser = argparse.ArgumentParser(description="AQUARYS Ingestion Script")
    parser.add_argument("--live", action="store_true", help="Ingest from live OAH API")
    parser.add_argument("--snapshot", action="store_true", help="Ingest from offline snapshots (default)")
    args = parser.parse_args()

    if args.live:
        asyncio.run(ingest_live())
    else:
        ingest_snapshot()


if __name__ == "__main__":
    main()
