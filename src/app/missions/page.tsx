"use client";

import { useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { useSites } from "@/hooks/use-sites";
import { useOptimizeMission } from "@/hooks/use-missions";
import { MOCK_MISSION, MOCK_FHIR_BUNDLE } from "@/lib/mock-data";
import { Mission, FHIRBundle } from "@/lib/types";
import { MissionBuilder } from "@/components/missions/MissionBuilder";
import { MissionMap } from "@/components/missions/MissionMap";
import { VolunteerAssignment } from "@/components/missions/VolunteerAssignment";
import { MissionImpact } from "@/components/missions/MissionImpact";
import { FHIRExportModal } from "@/components/export/FHIRExportModal";
import { Compass, Sparkles, Radio, ShieldAlert } from "lucide-react";
import { motion } from "motion/react";

function MissionsContent() {
  const searchParams = useSearchParams();
  const initialSiteId = searchParams.get("siteId") || "site-c1";

  const { data: sites = [] } = useSites();
  const [selectedSiteId, setSelectedSiteId] = useState(initialSiteId);
  const [currentMission, setCurrentMission] = useState<Mission>(MOCK_MISSION);
  const [selectedTaskId, setSelectedTaskId] = useState<string | undefined>(
    MOCK_MISSION.tasks?.[0]?.id
  );

  const [fhirModalOpen, setFhirModalOpen] = useState(false);
  const [fhirBundle, setFhirBundle] = useState<FHIRBundle>(MOCK_FHIR_BUNDLE);

  const optimizeMutation = useOptimizeMission();

  const handleOptimize = async (params: {
    siteId: string;
    objective: string;
    volunteerCount: number;
    timeAvailableMinutes: number;
  }) => {
    try {
      const result = await optimizeMutation.mutateAsync(params);
      setCurrentMission(result);
      if (result.tasks && result.tasks.length > 0) {
        setSelectedTaskId(result.tasks[0].id);
      }
    } catch {
      // Fallback remains active
    }
  };

  const handleTaskSelect = (taskId: string) => {
    setSelectedTaskId(taskId);
  };

  const handleOpenFhir = () => {
    setFhirModalOpen(true);
  };

  return (
    <div className="space-y-8 font-mono pb-16">
      {/* Page Header */}
      <div className="border-b border-slate-800 pb-6 flex flex-col md:flex-row md:items-end justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-bold uppercase tracking-wider text-xs mb-2">
            <Radio className="h-4 w-4 animate-pulse text-emerald-400" />
            <span>ALGORITHMIC FIELD CAMPAIGN & SAMPLING DISPATCH</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-white uppercase">
            Mission Control
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-2xl">
            Active sampling route optimization maximizing mutual information gain across environmental reaches.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleOpenFhir}
            className="px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 hover:border-cyan-500/50 text-slate-200 text-xs font-bold uppercase tracking-wider flex items-center gap-2 transition-colors"
          >
            <Sparkles className="h-3.5 w-3.5 text-cyan-400" />
            <span>FHIR R4 INTERCHANGE</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Parameters & Strategy */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Column: Mission Builder Configuration (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          <MissionBuilder
            sites={sites}
            selectedSiteId={selectedSiteId}
            onSiteChange={setSelectedSiteId}
            onOptimize={handleOptimize}
            isOptimizing={optimizeMutation.isPending}
          />

          {/* Active Mission Impact Overview */}
          <MissionImpact
            mission={currentMission}
            onExportFHIR={handleOpenFhir}
          />
        </div>

        {/* Right Column: Mission Map & Task Sequences (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          {/* Geospatial Map */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-300 uppercase">
                <Compass className="h-3.5 w-3.5 text-cyan-400" />
                <span>FIELD SAMPLING REACH TOPOLOGY</span>
              </div>
              <span className="text-[10px] text-slate-500 uppercase">
                {currentMission.tasks?.length || 0} COORDINATED STATIONS
              </span>
            </div>

            <MissionMap
              mission={currentMission}
              selectedTaskId={selectedTaskId}
              onTaskSelect={handleTaskSelect}
            />
          </div>

          {/* Volunteer Assignment Sequencing */}
          <VolunteerAssignment
            tasks={currentMission.tasks || []}
            selectedTaskId={selectedTaskId}
            onSelectTask={handleTaskSelect}
          />
        </div>
      </div>

      {/* Interoperable FHIR Export Modal */}
      <FHIRExportModal
        bundle={fhirBundle}
        isOpen={fhirModalOpen}
        onClose={() => setFhirModalOpen(false)}
        title={`FHIR R4 DISPATCH BUNDLE · ${currentMission.id.toUpperCase()}`}
      />
    </div>
  );
}

export default function MissionsPage() {
  return (
    <Suspense
      fallback={
        <div className="p-12 text-center font-mono text-xs text-slate-500">
          INITIALIZING MISSION CONTROL ENGINE...
        </div>
      }
    >
      <MissionsContent />
    </Suspense>
  );
}
