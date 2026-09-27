"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useEvaluateTrust() {
  return useMutation({
    mutationFn: (observationId: string) => api.evaluateTrust(observationId)
  });
}

export function useExportFHIR() {
  return useMutation({
    mutationFn: (siteId: string) => api.exportFHIR(siteId)
  });
}

export function useEvidenceGraph(id: string) {
  return useQuery({
    queryKey: ["evidence-graph", id],
    queryFn: () => api.getEvidenceGraph(id),
    enabled: !!id
  });
}
