"""SQLAlchemy models for AQUARYS entity definitions."""

import json
from datetime import UTC, datetime
from typing import Any, Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    TypeDecorator,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from aquarys.core.database import Base


class JSONType(TypeDecorator):
    """Platform-independent JSON type (JSON / JSONB on Postgres, Text on SQLite)."""

    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        if value is not None:
            return json.dumps(value)
        return None

    def process_result_value(self, value: Any, dialect: Any) -> Any:
        if value is not None:
            if isinstance(value, (dict, list)):
                return value
            return json.loads(value)
        return None


class VectorType(TypeDecorator):
    """Platform-independent embedding vector type."""

    impl = Text
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        if value is not None:
            if isinstance(value, list):
                return json.dumps([float(x) for x in value])
            return json.dumps(value)
        return None

    def process_result_value(self, value: Any, dialect: Any) -> list[float] | None:
        if value is not None:
            if isinstance(value, list):
                return [float(x) for x in value]
            return [float(x) for x in json.loads(value)]
        return None


def utcnow() -> datetime:
    return datetime.now(UTC)


class ProcessingRun(Base):
    """Record of an ingestion, normalization, or processing run."""

    __tablename__ = "processing_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    run_type: Mapped[str] = mapped_column(
        String(64), index=True
    )  # live_ingest, snapshot_ingest, fingerprint_eval
    status: Mapped[str] = mapped_column(String(32), default="started")  # started, completed, failed
    items_processed: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class Site(Base):
    """Research or urban stream monitoring site."""

    __tablename__ = "sites"

    id: Mapped[str] = mapped_column(
        String(64), primary_key=True
    )  # e.g., "PT-COI-C1" or OAH site id
    code: Mapped[str] = mapped_column(String(32), index=True)  # "C1", "G7", "L1"
    name: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(128), index=True)  # "Coimbra", "Ghent", "Lisbon"
    country: Mapped[str] = mapped_column(String(64), default="Portugal")
    stream_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float, index=True)
    altitude_m: Mapped[float | None] = mapped_column(Float, nullable=True)
    catchment_area_km2: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_hero: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Provenance
    source: Mapped[str] = mapped_column(String(64), default="OAH")
    source_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    raw_payload_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    processing_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)

    # Relationships
    observations: Mapped[list["Observation"]] = relationship(
        "Observation", back_populates="site", cascade="all, delete-orphan"
    )
    measurements: Mapped[list["Measurement"]] = relationship(
        "Measurement", back_populates="site", cascade="all, delete-orphan"
    )
    eo_measurements: Mapped[list["EOMeasurement"]] = relationship(
        "EOMeasurement", back_populates="site", cascade="all, delete-orphan"
    )
    profile: Mapped[Optional["StreamProfile"]] = relationship(
        "StreamProfile", back_populates="site", uselist=False, cascade="all, delete-orphan"
    )


class Observation(Base):
    """Citizen or field observation record."""

    __tablename__ = "observations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    site_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    observer_type: Mapped[str] = mapped_column(
        String(32), default="citizen"
    )  # citizen, researcher, sensor
    observer_id: Mapped[str | None] = mapped_column(String(128), nullable=True)

    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    # Qualitative & categorical observation data
    water_clarity: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )  # clear, turbid, cloudy, foamy
    flow_rate_category: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )  # dry, stagnant, slow, moderate, torrential
    odor: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )  # none, earthy, sewage, chemical
    algae_coverage_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    litter_present: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    canopy_cover_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    image_urls: Mapped[list[str]] = mapped_column(JSONType, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Provenance
    source: Mapped[str] = mapped_column(String(64), default="OAH")
    source_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    raw_payload_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    processing_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)

    # Relationships
    site: Mapped["Site"] = relationship("Site", back_populates="observations")
    assessment: Mapped[Optional["EvidenceAssessment"]] = relationship(
        "EvidenceAssessment",
        back_populates="observation",
        uselist=False,
        cascade="all, delete-orphan",
    )


class Measurement(Base):
    """Quantitative environmental / chemical / biological measurement."""

    __tablename__ = "measurements"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    site_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    parameter: Mapped[str] = mapped_column(
        String(64), index=True
    )  # dissolved_oxygen, ph, temperature, nitrate, conductivity
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(32))  # mg/L, °C, uS/cm, pH
    quality_flag: Mapped[str] = mapped_column(
        String(32), default="good"
    )  # good, suspect, derived, missing
    device_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Provenance
    source: Mapped[str] = mapped_column(String(64), default="OAH")
    source_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    raw_payload_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    processing_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)

    site: Mapped["Site"] = relationship("Site", back_populates="measurements")


class EOMeasurement(Base):
    """Earth Observation / Satellite derived measurement."""

    __tablename__ = "eo_measurements"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    site_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    satellite_source: Mapped[str] = mapped_column(String(64), default="Sentinel-2")
    ndvi: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Normalized Difference Vegetation Index
    ndwi: Mapped[float | None] = mapped_column(
        Float, nullable=True
    )  # Normalized Difference Water Index
    surface_temp_c: Mapped[float | None] = mapped_column(Float, nullable=True)
    cloud_cover_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    resolution_m: Mapped[float | None] = mapped_column(Float, default=10.0)

    # Provenance
    source: Mapped[str] = mapped_column(String(64), default="OAH-EO")
    source_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_endpoint: Mapped[str | None] = mapped_column(String(255), nullable=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    raw_payload_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    processing_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    metadata_json: Mapped[dict] = mapped_column(JSONType, default=dict)

    site: Mapped["Site"] = relationship("Site", back_populates="eo_measurements")


class EvidenceAssessment(Base):
    """Evidence Passport evaluation of an observation or measurement set."""

    __tablename__ = "evidence_assessments"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    observation_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("observations.id", ondelete="CASCADE"), unique=True, index=True
    )
    evaluated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    # 7-Dimensional Trust Evaluation Metrics
    completeness: Mapped[float] = mapped_column(Float, default=1.0)
    consistency: Mapped[float] = mapped_column(Float, default=1.0)
    location_validity: Mapped[float] = mapped_column(Float, default=1.0)
    temporal_validity: Mapped[float] = mapped_column(Float, default=1.0)
    image_support: Mapped[float] = mapped_column(Float, default=0.0)
    cross_observer: Mapped[float] = mapped_column(Float, default=0.0)
    independent_support: Mapped[float] = mapped_column(Float, default=0.0)
    duplicate_risk: Mapped[float] = mapped_column(Float, default=0.0)
    overall_confidence: Mapped[float] = mapped_column(Float, default=0.85)

    flags: Mapped[list[str]] = mapped_column(
        JSONType, default=list
    )  # e.g., ["NO_RECENT_CHEMICAL_CONFIRMATION"]
    positive_signals: Mapped[list[str]] = mapped_column(JSONType, default=list)
    negative_signals: Mapped[list[str]] = mapped_column(JSONType, default=list)
    reasoning: Mapped[str] = mapped_column(Text, default="")
    processing_version: Mapped[str] = mapped_column(String(32), default="1.0.0")

    observation: Mapped["Observation"] = relationship("Observation", back_populates="assessment")


class StreamProfile(Base):
    """9-Dimensional ecological fingerprint of a stream monitoring site."""

    __tablename__ = "stream_profiles"

    site_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), primary_key=True
    )
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    # Dimensions (0.0 to 100.0 or normalized score, None if missing)
    water_quality_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    habitat_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    vegetation_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    hydromorphology_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    biotics_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    nutrients_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    eo_context_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    citizen_evidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    climate_context_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Dimension status tracking (observed, derived, estimated, missing)
    dimension_status: Mapped[dict] = mapped_column(JSONType, default=dict)
    data_coverage_pct: Mapped[float] = mapped_column(Float, default=0.0)
    evidence_confidence_pct: Mapped[float] = mapped_column(Float, default=0.0)

    site: Mapped["Site"] = relationship("Site", back_populates="profile")
    embedding: Mapped[Optional["StreamEmbedding"]] = relationship(
        "StreamEmbedding", back_populates="profile", uselist=False, cascade="all, delete-orphan"
    )


class StreamEmbedding(Base):
    """Vector representation of stream fingerprint for rapid twin search."""

    __tablename__ = "stream_embeddings"

    site_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("stream_profiles.site_id", ondelete="CASCADE"), primary_key=True
    )
    vector: Mapped[list[float]] = mapped_column(VectorType)  # 32-dim or 64-dim embedding
    embedding_version: Mapped[str] = mapped_column(String(32), default="v1-deterministic")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    profile: Mapped["StreamProfile"] = relationship("StreamProfile", back_populates="embedding")


class StreamSimilarity(Base):
    """Precomputed or cached twin similarity between two stream sites."""

    __tablename__ = "stream_similarities"

    id: Mapped[str] = mapped_column(String(128), primary_key=True)  # "{site_a}_{site_b}"
    site_a_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    site_b_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )

    overall_similarity: Mapped[float] = mapped_column(Float)
    vector_similarity: Mapped[float] = mapped_column(Float)
    feature_similarity: Mapped[float] = mapped_column(Float)
    temporal_alignment: Mapped[float] = mapped_column(Float)
    data_coverage: Mapped[float] = mapped_column(Float)
    evidence_confidence: Mapped[float] = mapped_column(Float)

    match_signals: Mapped[dict] = mapped_column(JSONType, default=dict)
    differentiators: Mapped[list[str]] = mapped_column(JSONType, default=list)
    calculated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class EvidenceNode(Base):
    """Node in the relational Evidence Graph."""

    __tablename__ = "evidence_nodes"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    node_type: Mapped[str] = mapped_column(
        String(32), index=True
    )  # CLAIM, OBSERVATION, MEASUREMENT, EO_SIGNAL, SITE, HYPOTHESIS, INTERVENTION
    label: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    source_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)
    properties: Mapped[dict] = mapped_column(JSONType, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class EvidenceEdge(Base):
    """Directed edge in the relational Evidence Graph."""

    __tablename__ = "evidence_edges"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    source_node_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("evidence_nodes.id", ondelete="CASCADE"), index=True
    )
    target_node_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("evidence_nodes.id", ondelete="CASCADE"), index=True
    )
    edge_type: Mapped[str] = mapped_column(
        String(32), index=True
    )  # supports, contradicts, derived_from, correlates, located_at
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class OracleInvestigation(Base):
    """Grounded Oracle investigation record."""

    __tablename__ = "oracle_investigations"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    site_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    question: Mapped[str] = mapped_column(Text)
    finding: Mapped[str] = mapped_column(Text)
    facts: Mapped[list[str]] = mapped_column(JSONType, default=list)
    hypotheses: Mapped[list[dict]] = mapped_column(JSONType, default=list)
    counter_evidence: Mapped[list[str]] = mapped_column(JSONType, default=list)
    data_gaps: Mapped[list[dict]] = mapped_column(JSONType, default=list)
    next_observations: Mapped[list[dict]] = mapped_column(JSONType, default=list)
    caveats: Mapped[list[str]] = mapped_column(JSONType, default=list)
    evidence_ids: Mapped[list[str]] = mapped_column(JSONType, default=list)
    activity_events: Mapped[list[dict]] = mapped_column(JSONType, default=list)
    provider_used: Mapped[str] = mapped_column(String(64), default="demo")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Hypothesis(Base):
    """Specific hypothesis formulated during an investigation."""

    __tablename__ = "hypotheses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    investigation_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("oracle_investigations.id", ondelete="CASCADE"), index=True
    )
    statement: Mapped[str] = mapped_column(Text)
    plausibility_score: Mapped[float] = mapped_column(Float, default=0.7)
    supporting_evidence_ids: Mapped[list[str]] = mapped_column(JSONType, default=list)
    counter_evidence: Mapped[str | None] = mapped_column(Text, nullable=True)
    skeptic_challenge: Mapped[str | None] = mapped_column(Text, nullable=True)
    remaining_uncertainty: Mapped[str | None] = mapped_column(Text, nullable=True)


class Mission(Base):
    """Optimized volunteer field observation campaign."""

    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    objective: Mapped[str] = mapped_column(String(255))
    target_site_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("sites.id", ondelete="CASCADE"), index=True
    )
    volunteer_count: Mapped[int] = mapped_column(Integer, default=5)
    available_time_minutes: Mapped[int] = mapped_column(Integer, default=60)
    expected_information_gain: Mapped[float] = mapped_column(Float, default=0.0)
    coverage_improvement_pct: Mapped[float] = mapped_column(Float, default=0.0)
    gaps_addressed: Mapped[list[str]] = mapped_column(JSONType, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    tasks: Mapped[list["MissionTask"]] = relationship(
        "MissionTask", back_populates="mission", cascade="all, delete-orphan"
    )


class MissionTask(Base):
    """Task assigned to a specific volunteer within a mission."""

    __tablename__ = "mission_tasks"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    mission_id: Mapped[str] = mapped_column(
        String(64), ForeignKey("missions.id", ondelete="CASCADE"), index=True
    )
    volunteer_index: Mapped[int] = mapped_column(Integer)
    volunteer_name: Mapped[str] = mapped_column(String(64))  # e.g., "Volunteer 1"
    target_location_name: Mapped[str] = mapped_column(String(128))  # "C1 Upstream"
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    target_observation_type: Mapped[str] = mapped_column(
        String(64)
    )  # "Vegetation & Riparian Structure"
    priority: Mapped[str] = mapped_column(String(32), default="HIGH")  # HIGH, MEDIUM, LOW
    estimated_duration_min: Mapped[int] = mapped_column(Integer, default=15)
    expected_gain: Mapped[float] = mapped_column(Float, default=0.25)
    instructions: Mapped[str] = mapped_column(Text)

    mission: Mapped["Mission"] = relationship("Mission", back_populates="tasks")


class KnowledgeDocument(Base):
    """Domain knowledge or scientific reference document for evidence synthesis."""

    __tablename__ = "knowledge_documents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str] = mapped_column(
        String(64), index=True
    )  # urban_stream_syndrome, riparian_restoration, oah_protocol
    content: Mapped[str] = mapped_column(Text)
    doi_or_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
