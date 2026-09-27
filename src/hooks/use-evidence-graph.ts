"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useEvidenceGraph(id: string) {
  return useQuery({
    queryKey: ["evidenceGraph", id],
    queryFn: () => api.getEvidenceGraph(id),
    enabled: !!id
  });
}
