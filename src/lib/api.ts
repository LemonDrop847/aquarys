import {
  Site,
  Observation,
  EvidenceProfile,
  StreamFingerprint,
  TwinMatch,
  TwinComparison,
  TimelinePoint,
  OracleInvestigation,
  EvidenceGraph,
  Mission,
  FHIRBundle
} from "./types";
import {
  MOCK_SITES,
  MOCK_OBSERVATIONS,
  MOCK_EVIDENCE_PROFILE,
  MOCK_STREAM_FINGERPRINTS,
  MOCK_TWIN_MATCHES,
  MOCK_TWIN_COMPARISON,
  MOCK_ORACLE_INVESTIGATION,
  MOCK_EVIDENCE_GRAPH,
  MOCK_MISSION,
  MOCK_FHIR_BUNDLE
} from "./mock-data";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";
const IS_DEMO = process.env.NEXT_PUBLIC_DEMO_MODE === "true" || !API_BASE;

// Simulated network latency helper for smooth realistic feel in demo mode
const delay = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const api = {
  async getSites(): Promise<Site[]> {
    if (IS_DEMO) {
      await delay(200);
      return MOCK_SITES;
    }
    try {
      const res = await fetch(`${API_BASE}/api/sites`);
      if (!res.ok) throw new Error("Failed to fetch sites");
      return res.json();
    } catch {
      return MOCK_SITES;
    }
  },

  async getSite(id: string): Promise<Site | undefined> {
    if (IS_DEMO) {
      await delay(150);
      return MOCK_SITES.find((s) => s.id === id || s.code.toLowerCase() === id.toLowerCase()) || MOCK_SITES[0];
    }
    try {
      const res = await fetch(`${API_BASE}/api/sites/${id}`);
      if (!res.ok) throw new Error("Failed to fetch site");
      return res.json();
    } catch {
      return MOCK_SITES.find((s) => s.id === id || s.code.toLowerCase() === id.toLowerCase()) || MOCK_SITES[0];
    }
  },

  async getSiteFingerprint(id: string): Promise<StreamFingerprint> {
    if (IS_DEMO) {
      await delay(200);
      return MOCK_STREAM_FINGERPRINTS[id] || MOCK_STREAM_FINGERPRINTS["site-c1"];
    }
    try {
      const res = await fetch(`${API_BASE}/api/sites/${id}/fingerprint`);
      if (!res.ok) throw new Error("Failed to fetch fingerprint");
      return res.json();
    } catch {
      return MOCK_STREAM_FINGERPRINTS[id] || MOCK_STREAM_FINGERPRINTS["site-c1"];
    }
  },

  async getSiteTimeline(id: string): Promise<TimelinePoint[]> {
    const mockPoints: TimelinePoint[] = MOCK_TWIN_COMPARISON.timeline.map((point) => ({
      date: `${point.timestamp}-01`,
      value: point.siteAValue,
      metric: "Evidence Health Index",
      confidence: 92
    }));

    if (IS_DEMO) {
      await delay(150);
      return mockPoints;
    }
    try {
      const res = await fetch(`${API_BASE}/api/sites/${id}/timeline`);
      if (!res.ok) throw new Error("Failed to fetch timeline");
      return res.json();
    } catch {
      return mockPoints;
    }
  },

  async getObservations(siteId?: string): Promise<Observation[]> {
    if (IS_DEMO) {
      await delay(200);
      if (siteId) {
        return MOCK_OBSERVATIONS.filter((o) => o.siteId === siteId);
      }
      return MOCK_OBSERVATIONS;
    }
    try {
      const url = siteId ? `${API_BASE}/api/observations?siteId=${siteId}` : `${API_BASE}/api/observations`;
      const res = await fetch(url);
      if (!res.ok) throw new Error("Failed to fetch observations");
      return res.json();
    } catch {
      return MOCK_OBSERVATIONS;
    }
  },

  async getObservation(id: string): Promise<Observation | undefined> {
    if (IS_DEMO) {
      await delay(150);
      return MOCK_OBSERVATIONS.find((o) => o.id === id) || MOCK_OBSERVATIONS[0];
    }
    try {
      const res = await fetch(`${API_BASE}/api/observations/${id}`);
      if (!res.ok) throw new Error("Failed to fetch observation");
      return res.json();
    } catch {
      return MOCK_OBSERVATIONS[0];
    }
  },

  async evaluateTrust(observationId: string): Promise<EvidenceProfile> {
    if (IS_DEMO) {
      await delay(350);
      return {
        ...MOCK_EVIDENCE_PROFILE,
        observationId
      };
    }
    try {
      const res = await fetch(`${API_BASE}/api/trust/evaluate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ observationId })
      });
      if (!res.ok) throw new Error("Failed to evaluate trust");
      return res.json();
    } catch {
      return MOCK_EVIDENCE_PROFILE;
    }
  },

  async findTwins(siteId: string): Promise<TwinMatch[]> {
    if (IS_DEMO) {
      await delay(400);
      return MOCK_TWIN_MATCHES;
    }
    try {
      const res = await fetch(`${API_BASE}/api/twins/search?siteId=${siteId}`);
      if (!res.ok) throw new Error("Failed to find twins");
      return res.json();
    } catch {
      return MOCK_TWIN_MATCHES;
    }
  },

  async compareSites(siteA: string, siteB: string): Promise<TwinComparison> {
    if (IS_DEMO) {
      await delay(350);
      const foundA = MOCK_SITES.find((s) => s.id === siteA || s.code.toLowerCase() === siteA.toLowerCase()) || MOCK_SITES[0];
      const foundB = MOCK_SITES.find((s) => s.id === siteB || s.code.toLowerCase() === siteB.toLowerCase()) || MOCK_SITES[1];
      return {
        ...MOCK_TWIN_COMPARISON,
        siteA: {
          code: foundA.code,
          name: foundA.name,
          country: foundA.country,
          basin: foundA.region || "Mondego Basin"
        },
        siteB: {
          code: foundB.code,
          name: foundB.name,
          country: foundB.country,
          basin: foundB.region || "Scheldt Basin"
        }
      };
    }
    try {
      const res = await fetch(`${API_BASE}/api/twins/compare?siteA=${siteA}&siteB=${siteB}`);
      if (!res.ok) throw new Error("Failed to compare sites");
      return res.json();
    } catch {
      return MOCK_TWIN_COMPARISON;
    }
  },

  async investigateOracle(payload: { siteId: string; question: string }): Promise<OracleInvestigation> {
    if (IS_DEMO) {
      await delay(600);
      return {
        ...MOCK_ORACLE_INVESTIGATION,
        siteId: payload.siteId,
        question: payload.question || MOCK_ORACLE_INVESTIGATION.question
      };
    }
    try {
      const res = await fetch(`${API_BASE}/api/oracle/investigate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("Failed to run oracle investigation");
      return res.json();
    } catch {
      return MOCK_ORACLE_INVESTIGATION;
    }
  },

  async challengeOracle(investigationId: string): Promise<{
    initialConfidence: number;
    revisedConfidence: number;
    alternativeHypotheses: string[];
    criticalCounterEvidence: string[];
    remainingUncertainties: string[];
  }> {
    if (IS_DEMO) {
      await delay(500);
      return {
        initialConfidence: 82,
        revisedConfidence: 68,
        alternativeHypotheses: [
          "Mediterranean seasonal drought baseflow reduction accounts for 40% of dissolved oxygen depletion.",
          "Localized stormwater culvert thermal pulses create intermittent thermal anomalies independent of canopy cover.",
          "Citizen sampling bias toward accessible sunny banks inflates apparent thermal exposure."
        ],
        criticalCounterEvidence: [
          "Upstream shaded station recorded 1.9°C higher temperature than expected during July heatwave.",
          "Storm culvert #4 discharges water at 23.4°C immediately after precipitation events."
        ],
        remainingUncertainties: [
          "Nutrient loading vs thermal stress relative attribution is unconstrained without 48h spectrophotometry.",
          "Hydraulic retention time during summer baseflow has ±35% model variance."
        ]
      };
    }
    try {
      const res = await fetch(`${API_BASE}/api/oracle/${investigationId}/challenge`, {
        method: "POST"
      });
      if (!res.ok) throw new Error("Failed to challenge oracle");
      return res.json();
    } catch {
      return {
        initialConfidence: 82,
        revisedConfidence: 68,
        alternativeHypotheses: [
          "Mediterranean seasonal drought baseflow reduction accounts for 40% of dissolved oxygen depletion.",
          "Localized stormwater culvert thermal pulses create intermittent thermal anomalies independent of canopy cover."
        ],
        criticalCounterEvidence: [
          "Upstream shaded station recorded 1.9°C higher temperature than expected during July heatwave."
        ],
        remainingUncertainties: [
          "Nutrient loading vs thermal stress relative attribution is unconstrained without 48h spectrophotometry."
        ]
      };
    }
  },

  async getEvidenceGraph(id: string): Promise<EvidenceGraph> {
    if (IS_DEMO) {
      await delay(250);
      return MOCK_EVIDENCE_GRAPH;
    }
    try {
      const res = await fetch(`${API_BASE}/api/evidence/${id}/graph`);
      if (!res.ok) throw new Error("Failed to fetch evidence graph");
      return res.json();
    } catch {
      return MOCK_EVIDENCE_GRAPH;
    }
  },

  async optimizeMission(payload: {
    siteId: string;
    objective: string;
    volunteerCount: number;
    timeAvailableMinutes: number;
  }): Promise<Mission> {
    if (IS_DEMO) {
      await delay(500);
      return {
        ...MOCK_MISSION,
        volunteerCount: payload.volunteerCount || 5,
        timeAvailableMinutes: payload.timeAvailableMinutes || 60,
        objective: payload.objective || MOCK_MISSION.objective
      };
    }
    try {
      const res = await fetch(`${API_BASE}/api/missions/optimize`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      if (!res.ok) throw new Error("Failed to optimize mission");
      return res.json();
    } catch {
      return MOCK_MISSION;
    }
  },

  async getMission(id: string): Promise<Mission | undefined> {
    if (IS_DEMO) {
      await delay(200);
      return MOCK_MISSION;
    }
    try {
      const res = await fetch(`${API_BASE}/api/missions/${id}`);
      if (!res.ok) throw new Error("Failed to fetch mission");
      return res.json();
    } catch {
      return MOCK_MISSION;
    }
  },

  async exportFHIR(siteId: string): Promise<FHIRBundle> {
    if (IS_DEMO) {
      await delay(300);
      return MOCK_FHIR_BUNDLE;
    }
    try {
      const res = await fetch(`${API_BASE}/api/export/fhir?siteId=${siteId}`);
      if (!res.ok) throw new Error("Failed to export FHIR bundle");
      return res.json();
    } catch {
      return MOCK_FHIR_BUNDLE;
    }
  }
};
