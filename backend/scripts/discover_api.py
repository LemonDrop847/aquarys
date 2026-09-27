#!/usr/bin/env python3
"""CLI script to discover OAH API endpoints."""

import asyncio
import sys
from pathlib import Path

# Add src to sys.path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from aquarys.services.ingestion.discovery import discover_oah_api


async def main():
    print("Running OAH API Discovery...")
    manifest = await discover_oah_api()
    print(f"Discovery complete. Found {len(manifest.get('endpoints', []))} endpoints.")
    print(f"Status: {manifest.get('status')}")


if __name__ == "__main__":
    asyncio.run(main())
