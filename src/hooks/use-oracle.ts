"use client";

import { useMutation } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useInvestigateOracle() {
  return useMutation({
    mutationFn: (payload: { siteId: string; question: string }) => api.investigateOracle(payload)
  });
}

export function useChallengeOracle() {
  return useMutation({
    mutationFn: (investigationId: string) => api.challengeOracle(investigationId)
  });
}
