"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useOptimizeMission() {
  return useMutation({
    mutationFn: (payload: {
      siteId: string;
      objective: string;
      volunteerCount: number;
      timeAvailableMinutes: number;
    }) => api.optimizeMission(payload)
  });
}

export function useMission(id: string) {
  return useQuery({
    queryKey: ["mission", id],
    queryFn: () => api.getMission(id),
    enabled: !!id
  });
}
