"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useTwins(siteId: string) {
  return useQuery({
    queryKey: ["twins", siteId],
    queryFn: () => api.findTwins(siteId),
    enabled: !!siteId
  });
}

export function useCompareSites(siteA: string, siteB: string) {
  return useQuery({
    queryKey: ["compare-sites", siteA, siteB],
    queryFn: () => api.compareSites(siteA, siteB),
    enabled: !!siteA && !!siteB
  });
}
