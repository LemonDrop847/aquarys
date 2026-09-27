"""API routers for AQUARYS."""

from aquarys.api.observations import router as observations_router
from aquarys.api.sites import router as sites_router

__all__ = ["sites_router", "observations_router"]
