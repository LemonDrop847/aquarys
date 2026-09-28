"""Canonical normalization service for OAH environmental and citizen data."""

from typing import Any

from aquarys.models import EOMeasurement, Measurement, Observation, Site
from aquarys.services.normalization.eo import normalize_eo_measurement
from aquarys.services.normalization.measurement import normalize_measurement
from aquarys.services.normalization.observation import normalize_observation
from aquarys.services.normalization.site import normalize_site


class CanonicalNormalizer:
    """Normalizes heterogeneous raw inputs into canonical dicts or SQLAlchemy models."""

    @staticmethod
    def normalize_site(raw: dict[str, Any], raw_payload_hash: str | None = None) -> dict[str, Any]:
        return normalize_site(raw, raw_payload_hash)

    @staticmethod
    def normalize_observation(
        raw: dict[str, Any], raw_payload_hash: str | None = None
    ) -> dict[str, Any]:
        return normalize_observation(raw, raw_payload_hash)

    @staticmethod
    def normalize_measurement(
        raw: dict[str, Any], raw_payload_hash: str | None = None
    ) -> dict[str, Any]:
        return normalize_measurement(raw, raw_payload_hash)

    @staticmethod
    def normalize_eo_measurement(
        raw: dict[str, Any], raw_payload_hash: str | None = None
    ) -> dict[str, Any]:
        return normalize_eo_measurement(raw, raw_payload_hash)

    @classmethod
    def to_site_model(cls, raw: dict[str, Any], raw_payload_hash: str | None = None) -> Site:
        data = cls.normalize_site(raw, raw_payload_hash)
        return Site(**data)

    @classmethod
    def to_observation_model(
        cls, raw: dict[str, Any], raw_payload_hash: str | None = None
    ) -> Observation:
        data = cls.normalize_observation(raw, raw_payload_hash)
        return Observation(**data)

    @classmethod
    def to_measurement_model(
        cls, raw: dict[str, Any], raw_payload_hash: str | None = None
    ) -> Measurement:
        data = cls.normalize_measurement(raw, raw_payload_hash)
        return Measurement(**data)

    @classmethod
    def to_eo_measurement_model(
        cls, raw: dict[str, Any], raw_payload_hash: str | None = None
    ) -> EOMeasurement:
        data = cls.normalize_eo_measurement(raw, raw_payload_hash)
        return EOMeasurement(**data)

    @classmethod
    def normalize_batch(
        cls, entity_type: str, items: list[dict[str, Any]], raw_payload_hash: str | None = None
    ) -> list[dict[str, Any]]:
        if entity_type in ("sites", "site"):
            return [cls.normalize_site(item, raw_payload_hash) for item in items]
        if entity_type in ("observations", "observation"):
            return [cls.normalize_observation(item, raw_payload_hash) for item in items]
        if entity_type in ("measurements", "measurement"):
            return [cls.normalize_measurement(item, raw_payload_hash) for item in items]
        if entity_type in ("eo_measurements", "eo", "eo_measurement"):
            return [cls.normalize_eo_measurement(item, raw_payload_hash) for item in items]
        raise ValueError(f"Unknown entity_type: {entity_type}")


__all__ = [
    "CanonicalNormalizer",
    "normalize_site",
    "normalize_observation",
    "normalize_measurement",
    "normalize_eo_measurement",
]
