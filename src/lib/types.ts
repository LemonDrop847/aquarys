// Core domain types for AQUARYS frontend

export interface Site {
  id: string;
  name: string;
  code: string;
  latitude: number;
  longitude: number;
  country: string;
  region: string;
  observationCount: number;
  lastObserved: string; // ISO date
  evidenceCoverage: number; // 0-100
  knowledgeGaps: number;
}

export interface Observation {
  id: string;
  siteId: string;
  observedAt: string; // ISO datetime
  type: string; // e.g., "water_quality", "habitat", "citizen_report"
  value: string | number | Record<string, unknown>;
  unit?: string;
  confidence: number; // 0-100
  source: string; // e.g., "oah", "citizen", "eo"
  sourceId?: string;
  notes?: string;
}

export interface EvidenceFlag {
  metric: string;
  score: number; // 0-100
  status: "complete" | "partial" | "warning" | "critical";
}

export interface EvidenceProfile {
  observationId: string;
  completeness: number;
  consistency: number;
  location: number;
  temporalValidity: number;
  imageSupport: number;
  crossObserver: number;
  independentSupport: number;
  flags: EvidenceFlag[];
  explanation: string;
  warnings: string[];
  timestamp: string; // ISO
}

export interface StreamFingerprint {
  siteId: string;
  water: number | null;
  habitat: number | null;
  vegetation: number | null;
  hydromorphology: number | null;
  biotics: number | null;
  nutrients: number | null;
  earthObservation: number | null;
  citizenObservations: number | null;
  dataStatuses: {
    water: "observed" | "derived" | "estimated" | "missing";
    habitat: "observed" | "derived" | "estimated" | "missing";
    vegetation: "observed" | "derived" | "estimated" | "missing";
    hydromorphology: "observed" | "derived" | "estimated" | "missing";
    biotics: "observed" | "derived" | "estimated" | "missing";
    nutrients: "observed" | "derived" | "estimated" | "missing";
    earthObservation: "observed" | "derived" | "estimated" | "missing";
    citizenObservations: "observed" | "derived" | "estimated" | "missing";
  };
  lastUpdated: string; // ISO
}

export interface TimelinePoint {
  date: string; // ISO
  value: number;
  metric: string;
  confidence: number;
}

export interface TwinMatch {
  siteId: string;
  siteName: string;
  siteCode: string;
  similarity: number; // 0-100
  evidenceConfidence: number; // 0-100
  temporalAlignment: number; // 0-100
  matchSignals: {
    waterProfile: "strong" | "moderate" | "weak";
    habitatProfile: "strong" | "moderate" | "weak";
    eoContext: "strong" | "moderate" | "weak";
    temporalOverlap: "strong" | "moderate" | "weak";
  };
}

export interface TwinComparison {
  siteA: { code: string; name: string; country: string; basin: string };
  siteB: { code: string; name: string; country: string; basin: string };
  differentialMetrics: {
    metric: string;
    valueA: string | number;
    valueB: string | number;
    impact: "positive" | "warning" | "neutral";
  }[];
  differentiators: {
    title: string;
    description: string;
  }[];
  timeline: { timestamp: string; siteAValue: number; siteBValue: number }[];
}

export interface OracleActivity {
  step: number;
  label: string;
  status: "pending" | "complete" | "error";
  timestamp: string;
}

export interface OracleFact {
  id: string;
  statement: string;
  source: string;
  confidence: number;
}

export interface OracleHypothesis {
  id: string;
  statement: string;
  supportingEvidence: string[];
  counterEvidence: string[];
  confidence: number;
}

export interface OracleGap {
  id: string;
  description: string;
  impactOnUncertainty: string;
  suggestedObservation: string;
}

export interface NextObservation {
  description: string;
  location: string;
  expectedInformationGain: number;
  priority: "high" | "medium" | "low";
}

export interface OracleFinding {
  id: string;
  synthesis: string;
  confidence: number;
  supportingTwins: string[];
  evidenceCitations: Array<{ id: string; title: string; source: string; confidence: number }>;
  hypotheses: Array<{ id: string; title: string; description: string; confidence: number; supportingEvidenceCount: number }>;
  counterEvidence: Array<{ severity: string; description: string }>;
  knowledgeGaps: Array<{ dimension: string; impact: string; description: string }>;
  nextObservations: Array<{ location: string; expectedGain: number; targetMetric: string; rationale: string; protocol: string }>;
}

export interface OracleInvestigation {
  id: string;
  siteId: string;
  question: string;
  activity: OracleActivity[];
  findings: string;
  facts: OracleFact[];
  hypotheses: OracleHypothesis[];
  counterEvidence: string[];
  dataGaps: OracleGap[];
  nextObservations: NextObservation[];
  caveats: string;
  timestamp: string;
}

export interface EvidenceNode {
  id: string;
  type: "claim" | "observation" | "measurement" | "eo_signal" | "site" | "hypothesis" | "intervention";
  label: string;
  description?: string;
  confidence?: number;
  source?: string;
  sourceId?: string;
  observedAt?: string;
}

export interface EvidenceEdge {
  id: string;
  source: string;
  target: string;
  type: "supports" | "contradicts" | "derived_from" | "correlates" | "located_at";
  strength: number; // 0-100
}

export interface EvidenceGraph {
  id: string;
  claimId: string;
  nodes: EvidenceNode[];
  edges: EvidenceEdge[];
}

export interface Mission {
  id: string;
  name: string;
  objective: string;
  volunteerCount: number;
  timeAvailableMinutes: number;
  createdAt: string;
  tasks: MissionTask[];
  expectedInformationGain: number;
  coverageImprovement: number;
  knowledgeGapsAddressed: string[];
}

export interface MissionTask {
  id: string;
  siteId?: string;
  volunteerId: string;
  volunteerName: string;
  siteName: string;
  siteCode: string;
  location: string;
  latitude: number;
  longitude: number;
  observation: string;
  priority: "high" | "medium" | "low";
  estimatedDurationMinutes: number;
  informationGain: number;
}

export interface FHIRBundle {
  id?: string;
  resourceType: "Bundle";
  type: "collection";
  total: number;
  entry: Array<{
    resource: Record<string, unknown>;
  }>;
  meta?: {
    lastUpdated: string;
  };
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  timestamp: string;
}
