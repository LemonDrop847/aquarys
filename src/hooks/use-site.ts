"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useSite(id: string) {
  return useQuery({
    queryKey: ["site", id],
    queryFn: () => api.getSite(id),
    enabled: !!id
  });
}

export function useSiteFingerprint(id: string) {
  return useQuery({
    queryKey: ["site-fingerprint", id],
    queryFn: () => api.getSiteFingerprint(id),
    enabled: !!id
  });
}

export function useSiteTimeline(id: string) {
  return useQuery({
    queryKey: ["site-timeline", id],
    queryFn: () => api.getSiteTimeline(id),
    enabled: !!id
  });
}
