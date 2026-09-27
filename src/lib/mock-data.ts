import {
  Site,
  Observation,
  EvidenceProfile,
  StreamFingerprint,
  TwinMatch,
  TwinComparison,
  OracleInvestigation,
  EvidenceGraph,
  Mission,
  FHIRBundle
} from "./types";

export const MOCK_SITES: Site[] = [
  {
    id: "site-c1",
    name: "Rio Mondego - Coimbra Central",
    code: "C1",
    latitude: 40.2033,
    longitude: -8.4103,
    country: "Portugal",
    region: "Centro",
    observationCount: 38,
    lastObserved: "2026-09-24T14:30:00Z",
    evidenceCoverage: 91,
    knowledgeGaps: 3
  },
  {
    id: "site-g7",
    name: "Leie - Ghent Urban Basin",
    code: "G7",
    latitude: 51.0543,
    longitude: 3.7174,
    country: "Belgium",
    region: "Flanders",
    observationCount: 52,
    lastObserved: "2026-09-26T09:15:00Z",
    evidenceCoverage: 94,
    knowledgeGaps: 2
  },
  {
    id: "site-l4",
    name: "White Elster - Leipzig Süd",
    code: "L4",
    latitude: 51.3397,
    longitude: 12.3731,
    country: "Germany",
    region: "Saxony",
    observationCount: 29,
    lastObserved: "2026-09-22T11:45:00Z",
    evidenceCoverage: 83,
    knowledgeGaps: 5
  },
  {
    id: "site-b2",
    name: "Besòs River - Barcelona North",
    code: "B2",
    latitude: 41.4429,
    longitude: 2.2182,
    country: "Spain",
    region: "Catalonia",
    observationCount: 44,
    lastObserved: "2026-09-25T16:20:00Z",
    evidenceCoverage: 88,
    knowledgeGaps: 4
  },
  {
    id: "site-k9",
    name: "River Frome - Bristol Reach",
    code: "K9",
    latitude: 51.4545,
    longitude: -2.5879,
    country: "United Kingdom",
    region: "South West",
    observationCount: 31,
    lastObserved: "2026-09-21T08:10:00Z",
    evidenceCoverage: 79,
    knowledgeGaps: 6
  }
];

export const MOCK_OBSERVATIONS: Observation[] = [
  {
    id: "obs-101",
    siteId: "site-c1",
    observedAt: "2026-09-24T14:30:00Z",
    type: "Water Temperature & Dissolved Oxygen",
    value: "18.4°C / 7.2 mg/L DO",
    confidence: 94,
    source: "OAH In-Situ Sensor Probe",
    sourceId: "OAH-PR-40291",
    notes: "Continuous optical DO probe telemetry verified against lab calibration"
  },
  {
    id: "obs-102",
    siteId: "site-c1",
    observedAt: "2026-09-24T11:15:00Z",
    type: "Riparian Canopy Coverage",
    value: "42% Coverage",
    confidence: 88,
    source: "Sentinel-2 Multi-spectral NDVI",
    sourceId: "EO-S2-20260924",
    notes: "Derived 10m resolution canopy index with cloud cover < 2%"
  },
  {
    id: "obs-103",
    siteId: "site-c1",
    observedAt: "2026-09-23T17:40:00Z",
    type: "Macroinvertebrate Taxa Survey",
    value: "BMWP Score: 58 (Moderate biological quality)",
    confidence: 86,
    source: "OAH Field Biologist Protocol",
    sourceId: "OAH-BIO-9912",
    notes: "3-minute kick-sample across 3 micro-habitats (riffle, pool, vegetated margin)"
  },
  {
    id: "obs-104",
    siteId: "site-c1",
    observedAt: "2026-09-23T10:05:00Z",
    type: "Citizen Stream Visual Assessment",
    value: "Turbid plume detected downstream of storm culvert",
    confidence: 81,
    source: "Citizen Mobile App + Geotagged Image",
    sourceId: "CIT-REP-8831",
    notes: "EXIF verification confirms exact coordinates 40.2031° N, -8.4101° W"
  },
  {
    id: "obs-105",
    siteId: "site-c1",
    observedAt: "2026-09-20T09:00:00Z",
    type: "Orthophosphate & Nitrate Concentration",
    value: "NO3: 14.8 mg/L, PO4: 0.32 mg/L",
    confidence: 76,
    source: "Municipal Lab Spectrophotometry",
    sourceId: "LAB-COI-5510",
    notes: "Grab sample taken during baseflow conditions"
  }
];

export const MOCK_EVIDENCE_PROFILE: EvidenceProfile = {
  observationId: "obs-101",
  completeness: 100,
  consistency: 94,
  location: 91,
  temporalValidity: 97,
  imageSupport: 82,
  crossObserver: 87,
  independentSupport: 76,
  flags: [
    { metric: "Completeness", score: 100, status: "complete" },
    { metric: "Consistency", score: 94, status: "complete" },
    { metric: "Location Precision", score: 91, status: "complete" },
    { metric: "Temporal Validity", score: 97, status: "complete" },
    { metric: "Image Corroboration", score: 82, status: "partial" },
    { metric: "Cross-Observer Consensus", score: 87, status: "complete" },
    { metric: "Independent Chemical Verification", score: 76, status: "warning" }
  ],
  explanation: "Required metadata fields are 100% complete. Spatial telemetry aligns with target monitoring station. Two independent citizen reports within 150m and 3 hours corroborate elevated flow velocity.",
  warnings: [
    "No recent chemical spectrophotometric confirmation within the last 72 hours",
    "Single-operator optical DO sensor reading; cross-probe calibration offset is within ±0.15 mg/L"
  ],
  timestamp: "2026-09-24T14:35:00Z"
};

export const MOCK_STREAM_FINGERPRINTS: Record<string, StreamFingerprint> = {
  "site-c1": {
    siteId: "site-c1",
    water: 72,
    habitat: 42,
    vegetation: 48,
    hydromorphology: 38,
    biotics: 55,
    nutrients: 68,
    earthObservation: 84,
    citizenObservations: 91,
    dataStatuses: {
      water: "observed",
      habitat: "observed",
      vegetation: "derived",
      hydromorphology: "observed",
      biotics: "observed",
      nutrients: "derived",
      earthObservation: "observed",
      citizenObservations: "observed"
    },
    lastUpdated: "2026-09-24T14:30:00Z"
  },
  "site-g7": {
    siteId: "site-g7",
    water: 78,
    habitat: 74,
    vegetation: 76,
    hydromorphology: 70,
    biotics: 69,
    nutrients: 43,
    earthObservation: 88,
    citizenObservations: 83,
    dataStatuses: {
      water: "observed",
      habitat: "observed",
      vegetation: "observed",
      hydromorphology: "observed",
      biotics: "observed",
      nutrients: "observed",
      earthObservation: "observed",
      citizenObservations: "observed"
    },
    lastUpdated: "2026-09-26T09:15:00Z"
  },
  "site-l4": {
    siteId: "site-l4",
    water: 64,
    habitat: 52,
    vegetation: 61,
    hydromorphology: 45,
    biotics: null,
    nutrients: 72,
    earthObservation: 79,
    citizenObservations: 68,
    dataStatuses: {
      water: "observed",
      habitat: "derived",
      vegetation: "observed",
      hydromorphology: "estimated",
      biotics: "missing",
      nutrients: "observed",
      earthObservation: "observed",
      citizenObservations: "observed"
    },
    lastUpdated: "2026-09-22T11:45:00Z"
  },
  "site-b2": {
    siteId: "site-b2",
    water: 58,
    habitat: 40,
    vegetation: 36,
    hydromorphology: 31,
    biotics: 48,
    nutrients: 81,
    earthObservation: 86,
    citizenObservations: 89,
    dataStatuses: {
      water: "observed",
      habitat: "observed",
      vegetation: "derived",
      hydromorphology: "observed",
      biotics: "observed",
      nutrients: "observed",
      earthObservation: "observed",
      citizenObservations: "observed"
    },
    lastUpdated: "2026-09-25T16:20:00Z"
  },
  "site-k9": {
    siteId: "site-k9",
    water: 69,
    habitat: 58,
    vegetation: null,
    hydromorphology: 50,
    biotics: 61,
    nutrients: 55,
    earthObservation: 71,
    citizenObservations: 74,
    dataStatuses: {
      water: "observed",
      habitat: "observed",
      vegetation: "missing",
      hydromorphology: "observed",
      biotics: "observed",
      nutrients: "estimated",
      earthObservation: "derived",
      citizenObservations: "observed"
    },
    lastUpdated: "2026-09-21T08:10:00Z"
  }
};

export const MOCK_TWIN_MATCHES: TwinMatch[] = [
  {
    siteId: "site-g7",
    siteName: "Leie - Ghent Urban Basin",
    siteCode: "G7",
    similarity: 92,
    evidenceConfidence: 91,
    temporalAlignment: 83,
    matchSignals: {
      waterProfile: "strong",
      habitatProfile: "strong",
      eoContext: "moderate",
      temporalOverlap: "strong"
    }
  },
  {
    siteId: "site-b2",
    siteName: "Besòs River - Barcelona North",
    siteCode: "B2",
    similarity: 87,
    evidenceConfidence: 85,
    temporalAlignment: 79,
    matchSignals: {
      waterProfile: "strong",
      habitatProfile: "moderate",
      eoContext: "strong",
      temporalOverlap: "moderate"
    }
  },
  {
    siteId: "site-l4",
    siteName: "White Elster - Leipzig Süd",
    siteCode: "L4",
    similarity: 78,
    evidenceConfidence: 82,
    temporalAlignment: 74,
    matchSignals: {
      waterProfile: "moderate",
      habitatProfile: "weak",
      eoContext: "moderate",
      temporalOverlap: "strong"
    }
  },
  {
    siteId: "site-k9",
    siteName: "River Frome - Bristol Reach",
    siteCode: "K9",
    similarity: 73,
    evidenceConfidence: 77,
    temporalAlignment: 68,
    matchSignals: {
      waterProfile: "moderate",
      habitatProfile: "moderate",
      eoContext: "weak",
      temporalOverlap: "moderate"
    }
  }
];

export const MOCK_TWIN_COMPARISON: TwinComparison = {
  siteA: { code: "C1", name: "Rio Mondego", country: "Portugal", basin: "Mondego" },
  siteB: { code: "G7", name: "Leie Ghent", country: "Belgium", basin: "Scheldt" },
  differentialMetrics: [
    { metric: "Riparian structure", valueA: "42/100", valueB: "78/100", impact: "warning" },
    { metric: "Bank naturalness", valueA: "31/100", valueB: "74/100", impact: "warning" },
    { metric: "Biotic diversity", valueA: "55/100", valueB: "69/100", impact: "positive" },
    { metric: "Chemical stress", valueA: "68/100", valueB: "43/100", impact: "warning" },
    { metric: "Citizen evidence density", valueA: "91/100", valueB: "83/100", impact: "positive" },
    { metric: "EO thermal stability", valueA: "62/100", valueB: "86/100", impact: "warning" }
  ],
  differentiators: [
    {
      title: "Vegetative Buffer Continuity",
      description: "Site G7 maintains 85% continuous riparian buffer vs 28% at Site C1, moderating solar thermal input."
    },
    {
      title: "Substrate Naturalness & Meandering",
      description: "Site G7 features active gravel-bed dynamics and pool-riffle morphology vs concrete canalization at Site C1."
    }
  ],
  timeline: [
    { timestamp: "2026-05", siteAValue: 48, siteBValue: 68 },
    { timestamp: "2026-06", siteAValue: 44, siteBValue: 71 },
    { timestamp: "2026-07", siteAValue: 39, siteBValue: 73 },
    { timestamp: "2026-08", siteAValue: 41, siteBValue: 75 },
    { timestamp: "2026-09", siteAValue: 45, siteBValue: 78 }
  ]
};

export const MOCK_ORACLE_INVESTIGATION: OracleInvestigation = {
  id: "inv-9042",
  siteId: "site-c1",
  question: "What ecological trajectories and interventions can Rio Mondego (C1) learn from comparable urban stream basins?",
  activity: [
    { step: 1, label: "Retrieved observation set (38 validated records)", status: "complete", timestamp: "14:31:02" },
    { step: 2, label: "Evaluated evidentiary quality via Trust Fabric", status: "complete", timestamp: "14:31:05" },
    { step: 3, label: "Calculated multi-dimensional stream fingerprint", status: "complete", timestamp: "14:31:07" },
    { step: 4, label: "Identified comparable ecological twin: G7 (Ghent)", status: "complete", timestamp: "14:31:09" },
    { step: 5, label: "Compared temporal trajectories (May - Sept 2026)", status: "complete", timestamp: "14:31:11" },
    { step: 6, label: "Synthesized verified physical differences", status: "complete", timestamp: "14:31:13" },
    { step: 7, label: "Generated grounded ecological hypotheses", status: "complete", timestamp: "14:31:15" },
    { step: 8, label: "Checked counter-evidence & alternative explanations", status: "complete", timestamp: "14:31:17" },
    { step: 9, label: "Identified critical knowledge gaps & next observations", status: "complete", timestamp: "14:31:19" }
  ],
  findings: "Comparative analysis between Rio Mondego (C1) and Leie Ghent (G7) demonstrates that while baseline water chemistry is comparable (DO: 7.2 vs 7.8 mg/L), G7 exhibits a 36-point advantage in Riparian Structure (78 vs 42) and a 43-point advantage in Bank Naturalness (74 vs 31). Historical data from G7 indicates that its 2024 bank renaturalization and continuous vegetative buffering preceded a 22% reduction in thermal spikes and a 31% increase in macroinvertebrate diversity.",
  facts: [
    {
      id: "fact-1",
      statement: "C1 bank naturalness score is 31/100 due to extensive concrete canalization along the urban reach.",
      source: "OAH Hydromorphological Assessment Protocol #HM-2026-04",
      confidence: 94
    },
    {
      id: "fact-2",
      statement: "G7 Ghent recovered biological diversity score from 51 to 69 following the 2024 vegetated buffer restoration.",
      source: "Ghent Urban River Dataset / Flemish Environmental Agency",
      confidence: 96
    },
    {
      id: "fact-3",
      statement: "C1 macroinvertebrate taxa survey indicates BMWP score of 58 (moderate stress).",
      source: "OAH In-Situ Biology Field Sample #OAH-BIO-9912",
      confidence: 86
    }
  ],
  hypotheses: [
    {
      id: "hyp-1",
      statement: "Canopy shade restoration along the northern reach of C1 could reduce peak summer water temperatures by 1.5°C to 2.2°C, aligning thermal stability with G7.",
      supportingEvidence: [
        "EO Sentinel-2 thermal band indicates 3.4°C thermal gradient between shaded upstream and unshaded urban reach.",
        "Twin G7 thermal stability score is 86 vs C1 score of 62."
      ],
      counterEvidence: [
        "Urban stormwater culverts introduce high-temperature surface runoff regardless of riparian shading.",
        "Deep channel geometry at C1 limits maximum vegetative overhang to 28% of stream width."
      ],
      confidence: 82
    },
    {
      id: "hyp-2",
      statement: "Substrate gravel reintroduction at riffle sections could elevate macroinvertebrate BMWP score above 70 within two seasonal cycles.",
      supportingEvidence: [
        "G7 post-restoration monitoring demonstrated 14-point BMWP gain following gravel bar placement.",
        "Current C1 substrate is 68% silt-choked concrete slab."
      ],
      counterEvidence: [
        "High winter storm surge velocities in Rio Mondego may wash out unconsolidated gravel without upstream flow dampening.",
        "Nutrient loading (PO4: 0.32 mg/L) remains an independent stressor on sensitive Ephemeroptera taxa."
      ],
      confidence: 75
    }
  ],
  counterEvidence: [
    "Could seasonal Mediterranean drought explain the summer biological dip at C1 rather than structural bank degradation?",
    "Could citizen sampling frequency bias introduce apparent water quality anomalies during storm events?"
  ],
  dataGaps: [
    {
      id: "gap-1",
      description: "No continuous chemical spectrophotometry within 500m upstream of urban canalization intake.",
      impactOnUncertainty: "High - uncertainty on whether nutrient pulse originates from upstream agriculture or urban discharge.",
      suggestedObservation: "Deploy 48-hour automated multi-parameter sonde at C1 Upstream Bridge (40.2110° N, -8.4150° W)."
    },
    {
      id: "gap-2",
      description: "Substrate grain size distribution not sampled since May 2026.",
      impactOnUncertainty: "Medium - prevents precise hydraulic model of gravel stability during peak autumn storm flows.",
      suggestedObservation: "Perform Wolman pebble count (100-particle sample) across 3 transects at Site C1."
    }
  ],
  nextObservations: [
    {
      description: "Collect 3-transect Wolman pebble count and benthic sediment core sample",
      location: "Site C1 Upstream Transect (40.2085° N, -8.4120° W)",
      expectedInformationGain: 0.38,
      priority: "high"
    },
    {
      description: "Install 48h dissolved oxygen and temperature logger at stormwater outlet #4",
      location: "Site C1 Storm Culvert Outfall (40.2030° N, -8.4100° W)",
      expectedInformationGain: 0.29,
      priority: "high"
    },
    {
      description: "Citizen photographic survey of emergent macrophytes along south bank",
      location: "Site C1 South Bank Reach (40.2010° N, -8.4080° W)",
      expectedInformationGain: 0.18,
      priority: "medium"
    }
  ],
  caveats: "Findings are derived from retrospective twin matching and deterministic empirical telemetry. Environmental interventions must undergo local hydrological impact assessment prior to structural modifications.",
  timestamp: "2026-09-27T10:15:00Z"
};

export const MOCK_EVIDENCE_GRAPH: EvidenceGraph = {
  id: "graph-c1-9042",
  claimId: "claim-canopy-temperature",
  nodes: [
    {
      id: "node-1",
      type: "claim",
      label: "Canopy Deficit Induces Thermal Stress",
      description: "Lack of riparian canopy causes 3.4°C summer temperature spike in Rio Mondego urban reach.",
      confidence: 82
    },
    {
      id: "node-2",
      type: "measurement",
      label: "Sentinel-2 NDVI Canopy Cover: 42%",
      description: "Derived 10m resolution canopy index from multi-spectral imagery.",
      source: "ESA Sentinel-2",
      sourceId: "EO-S2-20260924",
      observedAt: "2026-09-24"
    },
    {
      id: "node-3",
      type: "observation",
      label: "In-Situ Water Temp: 18.4°C",
      description: "Calibrated optical telemetry probe at monitoring station.",
      source: "OAH In-Situ Sensor Probe",
      sourceId: "OAH-PR-40291",
      observedAt: "2026-09-24"
    },
    {
      id: "node-4",
      type: "eo_signal",
      label: "Landsat-9 Thermal Band: 24.1°C Skin Temp",
      description: "Surface skin temperature showing urban heat island effect over unshaded canal.",
      source: "USGS Landsat-9 TIRS",
      sourceId: "LC09-TIRS-20260920",
      observedAt: "2026-09-20"
    },
    {
      id: "node-5",
      type: "site",
      label: "Site C1: Rio Mondego Central",
      description: "Urban canalized stream reach in Coimbra, Portugal.",
      confidence: 91
    },
    {
      id: "node-6",
      type: "hypothesis",
      label: "Vegetative Buffer Reduces Thermal Peaks",
      description: "Riparian replanting modeled to drop water temp by 1.8°C based on G7 Ghent twin trajectory.",
      confidence: 78
    },
    {
      id: "node-7",
      type: "intervention",
      label: "Riparian Tree Planting Campaign",
      description: "2.4km native alder and willow planting along northern bank.",
      confidence: 85
    }
  ],
  edges: [
    { id: "e1-2", source: "node-2", target: "node-1", type: "supports", strength: 88 },
    { id: "e1-3", source: "node-3", target: "node-1", type: "supports", strength: 94 },
    { id: "e1-4", source: "node-4", target: "node-1", type: "supports", strength: 86 },
    { id: "e5-1", source: "node-5", target: "node-1", type: "located_at", strength: 100 },
    { id: "e1-6", source: "node-1", target: "node-6", type: "derived_from", strength: 80 },
    { id: "e6-7", source: "node-6", target: "node-7", type: "supports", strength: 85 }
  ]
};

export const MOCK_MISSION: Mission = {
  id: "mission-092",
  name: "Mondego Reach Uncertainty Reduction Campaign",
  objective: "Resolve critical thermal and sediment knowledge gaps across Site C1 and upstream tributaries",
  volunteerCount: 5,
  timeAvailableMinutes: 60,
  createdAt: "2026-09-27T08:00:00Z",
  expectedInformationGain: 0.84,
  coverageImprovement: 28,
  knowledgeGapsAddressed: [
    "Upstream nutrient baseline verification",
    "Substrate grain size distribution",
    "Emergent macrophyte spatial mapping",
    "Culvert thermal discharge verification"
  ],
  tasks: [
    {
      id: "task-1",
      volunteerId: "vol-1",
      volunteerName: "Volunteer 1 (Lead Hydrologist)",
      siteName: "Rio Mondego - C1 Upstream Bridge",
      siteCode: "C1-UP",
      location: "North Bridge Span (40.2085° N, -8.4120° W)",
      latitude: 40.2085,
      longitude: -8.4120,
      observation: "Conduct Wolman 100-pebble count along 30m riffle transect",
      priority: "high",
      estimatedDurationMinutes: 45,
      informationGain: 0.38
    },
    {
      id: "task-2",
      volunteerId: "vol-2",
      volunteerName: "Volunteer 2 (Field Specialist)",
      siteName: "Rio Mondego - C1 Storm Culvert",
      siteCode: "C1-OUT",
      location: "Storm Drain Outfall #4 (40.2030° N, -8.4100° W)",
      latitude: 40.2030,
      longitude: -8.4100,
      observation: "Optical temperature probe reading & turbidity test strip",
      priority: "high",
      estimatedDurationMinutes: 30,
      informationGain: 0.29
    },
    {
      id: "task-3",
      volunteerId: "vol-3",
      volunteerName: "Volunteer 3 (Citizen Observer)",
      siteName: "Rio Mondego - C1 South Bank",
      siteCode: "C1-SB",
      location: "South Promenade Reach (40.2010° N, -8.4080° W)",
      latitude: 40.2010,
      longitude: -8.4080,
      observation: "Geotagged photographic transect of emergent macrophyte patches",
      priority: "medium",
      estimatedDurationMinutes: 25,
      informationGain: 0.18
    },
    {
      id: "task-4",
      volunteerId: "vol-4",
      volunteerName: "Volunteer 4 (Citizen Observer)",
      siteName: "Rio Mondego - Santa Clara Tributary",
      siteCode: "C1-TRIB",
      location: "Confluence Point (40.1980° N, -8.4210° W)",
      latitude: 40.1980,
      longitude: -8.4210,
      observation: "Visual water clarity classification & floating debris tally",
      priority: "medium",
      estimatedDurationMinutes: 20,
      informationGain: 0.12
    },
    {
      id: "task-5",
      volunteerId: "vol-5",
      volunteerName: "Volunteer 5 (Citizen Observer)",
      siteName: "Rio Mondego - Downstream Weir",
      siteCode: "C1-WEIR",
      location: "Açude-Ponte Weir Barrier (40.1950° N, -8.4350° W)",
      latitude: 40.1950,
      longitude: -8.4350,
      observation: "Fish passage observation & surface foam accumulation assessment",
      priority: "low",
      estimatedDurationMinutes: 20,
      informationGain: 0.08
    }
  ]
};

export const MOCK_FHIR_BUNDLE: FHIRBundle = {
  resourceType: "Bundle",
  type: "collection",
  total: 5,
  meta: {
    lastUpdated: "2026-09-27T10:15:00Z"
  },
  entry: [
    {
      resource: {
        resourceType: "Location",
        id: "loc-c1-mondego",
        identifier: [{ system: "https://aquarys.intelligence/sites", value: "C1" }],
        status: "active",
        name: "Rio Mondego - Coimbra Central Monitoring Reach",
        position: {
          latitude: 40.2033,
          longitude: -8.4103
        }
      }
    },
    {
      resource: {
        resourceType: "Observation",
        id: "obs-water-temp-c1",
        status: "final",
        category: [
          {
            coding: [
              {
                system: "http://terminology.hl7.org/CodeSystem/observation-category",
                code: "laboratory",
                display: "Environmental Telemetry"
              }
            ]
          }
        ],
        code: {
          coding: [
            {
              system: "http://loinc.org",
              code: "8310-5",
              display: "Water Temperature"
            }
          ],
          text: "Water Temperature"
        },
        subject: { reference: "Location/loc-c1-mondego" },
        effectiveDateTime: "2026-09-24T14:30:00Z",
        valueQuantity: {
          value: 18.4,
          unit: "Cel",
          system: "http://unitsofmeasure.org",
          code: "Cel"
        },
        extension: [
          {
            url: "https://aquarys.intelligence/fhir/StructureDefinition/evidence-confidence",
            valueDecimal: 0.94
          },
          {
            url: "https://aquarys.intelligence/fhir/StructureDefinition/provenance-hash",
            valueString: "sha256-e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
          }
        ]
      }
    },
    {
      resource: {
        resourceType: "Observation",
        id: "obs-dissolved-oxygen-c1",
        status: "final",
        code: {
          coding: [
            {
              system: "http://loinc.org",
              code: "2713-6",
              display: "Dissolved Oxygen in Water"
            }
          ]
        },
        subject: { reference: "Location/loc-c1-mondego" },
        effectiveDateTime: "2026-09-24T14:30:00Z",
        valueQuantity: {
          value: 7.2,
          unit: "mg/L",
          system: "http://unitsofmeasure.org",
          code: "mg/L"
        }
      }
    },
    {
      resource: {
        resourceType: "RiskAssessment",
        id: "assessment-evidence-passport-c1",
        status: "final",
        subject: { reference: "Location/loc-c1-mondego" },
        occurrenceDateTime: "2026-09-27T10:15:00Z",
        basis: [{ reference: "Observation/obs-water-temp-c1" }],
        prediction: [
          {
            outcome: {
              text: "Evidence Completeness & Corroboration Passport"
            },
            probabilityDecimal: 0.91,
            rationale: "Completeness: 100%, Consistency: 94%, Location: 91%, Temporal: 97%"
          }
        ]
      }
    }
  ]
};
