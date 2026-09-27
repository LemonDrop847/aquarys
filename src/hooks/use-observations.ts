"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useObservations(siteId?: string) {
  return useQuery({
    queryKey: ["observations", siteId],
    queryFn: () => api.getObservations(siteId)
  });
}

export function useObservation(id: string) {
  return useQuery({
    queryKey: ["observation", id],
    queryFn: () => api.getObservation(id),
    enabled: !!id
  });
}
